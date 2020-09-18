from io import BytesIO

from dal import autocomplete
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic import View
from formtools.wizard.views import NamedUrlCookieWizardView
from xhtml2pdf import pisa

from guide.forms import (CftaExceptionForm, GeneralExceptionForm,
                         LimitedTenderingForm, RequiredFieldsForm)
from guide.models import (AGREEMENTS_FIELDS, CftaException, Code,
                          CodeOrganizationExclusion, CommodityType,
                          ConstructionCoverage, GeneralException,
                          GoodsCoverage, LimitedTenderingReason, Organization,
                          ValueThreshold)

FORMS = [("0", RequiredFieldsForm),
         ("1", GeneralExceptionForm),
         ("2", CftaExceptionForm),
         ("3", LimitedTenderingForm)]

TEMPLATES = {"0": "mandatory_elements.html",
             "1": "exceptions.html",
             "2": "cfta_exceptions.html",
             "3": "limited_tendering.html"}

url_name='guide:form_step'
done_step_name='guide:done_step'

def create_data_dict(self, forms):
    """The form wizard keeps the context data in a context dict.  
    We are taking in the forms and saving it in a dictionary.
    At the end this dictionary will be added to the context dict.

    Args:
        forms ([list]): List of forms

    Returns:
        [dict]: Dictionary with keys as form fields and values as user selected inputs
    """
    func_data_dict = {}
    try:
        for f in forms:
            func_data_dict.update(self.get_cleaned_data_for_step(f))
    except:
        pass
    return func_data_dict

def create_agreement_dict():
    """The form wizard keeps the context data in a context dict.  
    We are creating a dictionary where each trade agreement is a key.
    The value is an empty dictionary. Later we will be adding
    to the empty dictionary the form fields along with True or False
    for each field.  So it will look like {'cfta':{'entities': True, 'code': False...}}


    Returns:
        [dict]: Dictionary where each key is an agreement and the value is an empty dict.
    """
    func_agreement_dict = {k:{} for k in AGREEMENTS_FIELDS}
    return func_agreement_dict

def value_threshold_rule(agreement, data):
    """Each trade agreement has trade thresholds.  Above these thresholds the trade
    agreement applies, below this threshold the trade agreement does not apply.
    There are different thresholds for each agreement, and within each agreement there
    are different thresholds for each commodity type (Goods, Services, Construction).
    This function compares the user inputed value and commodity type with the info
    in the ValueThreshold model.  
    
    This function takes two dictionaries:
        1) the agreement dictionary has keys as trade agreements
            and the values are dictionaries.  In the nested dictionaries
            each key is a form field and the values are boolean.
        2_ the data dictionary has keys for each form field and 
            values as inputed user data.
    This function checks the threshold for each agreement against the input, 
    if the input value is below the agreement threshold then the trade agreement does 
    not apply and the agreement dictionary is updated to contain 'estimated_value' as 
    False.  We are not setting it to True in this function.

    Args:
        agreement ([dict]): Keys are trade agreements, values are dictionaries where the
            keys are form fields and the values are boolean.
        data ([dict]): Keys are form fields and values are the user inputted data.

    Returns:
        [dict]: Returns the agreement dictionary now it has been updated with
            any instances where 'estimated_value' is False.
    """
    model = ValueThreshold
    value = int(data['estimated_value'])
    type = data['type']
    for k in agreement.keys():
        threshold = model.objects.filter(type=type).values_list(k).get()[0]
        if value < threshold:
            agreement[k]['estimated_value'] = False
    return agreement

def organization_rule(agreement, data):
    """Each trade agreement has a list of entities that are covered or not
        covered by the agreement.
        This function takes two dictionaries:
            1) the agreement dictionary has keys as trade agreements
                and the values are dictionaries.  In the nested dictionaries
                each key is a form field and the values are boolean.
            2_ the data dictionary has keys for each form field and 
                values as inputed user data.

        This function gets the entity name from data dict and checks it against
        the Organization models.  For each agreement it checks if the entity is 
        covered (True) or not (False).  If it is false then the agreement dict
        is updated to False.  We are not setting true in this function.

    Args:
        agreement ([dict]): Keys are trade agreements, values are dictionaries where the
            keys are form fields and the values are boolean.
        data ([dict]): Keys are form fields and values are the user inputted data.

    Returns:
        [dict]: Returns the agreement dictionary now it has been updated with
            any instances where 'entities' is False.
    """
    org = data['entities']

    for k in agreement.keys():
        check = Organization.objects.filter(name=org).values_list(k).get()[0]
        if check:
            pass
        else:
            agreement[k]['entities'] = False

    return agreement

def construction_coverage(_agreement, org, code):
    """This function is triggered if the user has selected Construction
    as the commodity type. There is a special rule for construction,
    which is implemented by the model ConstructionCoverage.  For any
    entities listed in ConstructionCoverage no construction is covered.
    If the entity is not in ConstructionCoverage then it checks the Commodity
    Code table to see if the code the user selected is covered.   

    If the Entity is found in ConstructionCoverage or if the Code is not covered
    by the agreement then this function updates the agreement dictionary 'code' to False.
    We are not setting true here.

    Args:
        _agreement ([dict]): Keys are trade agreements, values are dictionaries where the
            keys are form fields and the values are boolean.
        org ([str]): Name of the entity the user selected.
        code ([str]): Name of the code the user selected.

    Returns:
        [dict]: Returns the agreement dictionary now it has been updated with
            any instances where 'code' is False.
    """

    code_db = Code.objects.filter(code=code)
    if ConstructionCoverage.objects.filter(org_fk=org).exists():
        for k in _agreement.keys():
            check = ConstructionCoverage.objects.filter(org_fk=org).values_list(k).get()[0]
            if check:
                _agreement[k]['code'] = False
    else:
        for k in _agreement.keys():
            check = code_db.values_list(k).get()[0]
            if not check:
                _agreement[k]['code'] = False
    return _agreement

def goods_coverage(_agreement, org, code):
    """This function is triggered if the user has selected Goods
    as the commodity type. There is a special rule for goods,
    which is implemented by the model GoodsCoverage.  For entities NOT 
    listed in GoodsCoverage then the goods commodity code is covered.  

    If the entity IS in GoodsCoverage then it checks the Commodity
    Code table to see if the code the user selected is covered.   

    If the Entity is found in GoodsCoverage and if the Code is not covered
    by the agreement then this function updates the agreement dictionary 'code' to False.
    We are not setting true here.

    Args:
        _agreement ([dict]): Keys are trade agreements, values are dictionaries where the
            keys are form fields and the values are boolean.
        org ([str]): Name of the entity the user selected.
        code ([str]): Name of the code the user selected.

    Returns:
        [dict]: Returns the agreement dictionary now it has been updated with
            any instances where 'code' is False.
    """
    code_db = Code.objects.filter(code=code)
    if GoodsCoverage.objects.filter(org_fk=org).exists():
        for k in _agreement.keys():
            check = code_db.values_list(k).get()[0]
            if not check:
                _agreement[k]['code'] = False
    return _agreement

def services_coverage(_agreement, code):
    """This function is triggered if the user has selected Services
    as the commodity type. This checks the code the user has entered and
    compares it to the code in the Commodity Code table.  For each agreement
    if the code is not covered we update the agreement dict to show that
    the 'code' is False.  We are not setting true here.  

    Args:
        _agreement ([dict]): Keys are trade agreements, values are dictionaries where the
            keys are form fields and the values are boolean.
        code ([str]): Name of the code the user selected.

    Returns:
        [dict]: Returns the agreement dictionary now it has been updated with
            any instances where 'code' is False.
    """
    code_db = Code.objects.filter(code=code)
    for k in _agreement.keys():
        check = code_db.values_list(k).get()[0]
        if not check:
            _agreement[k]['code'] = False
    return _agreement

def code_org_exclusion(_agreement, org, code):
    """This implements a trade rule that is a big complicated.
    In some agreements there is a carveout that says for
    Department X the Commodity Code Y is not covered. Usually
    commodity codes are covered or not covered for all entities
    in an agreement.

    The content for this is stored in the CodeOrganizationExclusion
    model.  This function checks if the organiztion selected and the
    code selected are found in that model.  If it is then it goes
    through and checks which agreements this exception is found.

    If it is found in an agreement then check is set to true.  Since
    this is an exclusion, if it is found that means the code is not
    covered.  So when check is set to true the 'code' is set to False.
    We are not setting 'code' to true here.

    Args:
        _agreement ([dict]): Keys are trade agreements, values are dictionaries where the
            keys are form fields and the values are boolean.
        org ([str]): Name of the entity the user selected.
        code ([str]): Name of the code the user selected.

    Returns:
        [dict]: Returns the agreement dictionary now it has been updated with
            any instances where 'code' is False.
    """
    if CodeOrganizationExclusion.objects.filter(org_fk=org).filter(code_fk=code).exists():

        for k in _agreement.keys():
            check = CodeOrganizationExclusion.objects.filter(org_fk=org).filter(code_fk=code).values_list(k).get()[0]
            if check:
                _agreement[k]['code'] = False
    return _agreement

def set_true(_agreement, field):
    """This takes a dict where keys are trade agreements and the values are
    dictionaries.  The other functions have been setting form fields as keys
    and values as False.  This function checks for each agreement and for
    each form field if the value False exists.  If it does not exist then
    it updates the dictionary by adding the form field as a key and the
    value as True.

    Args:
        _agreement ([dict]): Keys are trade agreements, values are dictionaries where the
            keys are form fields and the values are boolean.
        field ([list]): List of form fields, ['entities', 'code'...]

    Returns:
        [dict]: A dictionary containing keys as trade agreement and values as dicts.
        The nest dict have all the form fields as keys and a boolean as value.
    """
    for k in _agreement.keys():
        try: 
            _test = _agreement[k][field]
        except:
            _agreement[k][field] = True
    return _agreement

def exceptions_rule(agreement, data, exception):
    """There are two exceptions rules for this tool, General Exceptions, and
    CFTA Exceptions.  This function takes as arguments the user input and goes
    through each agreement and checks if that user-selected excepion exists
    in the agreement.  If the user-select exception exists in the 
    agreement then it creates a key for the exception and sets the value
    to false.

    First it unpacks a dictionary with exception_name ('exceptions', or
    'cfta_exceptions').  
    Second it gets the exception from the data dictionary. If no 
    exception is present this is an empty list.
    Third if checks if there is an exception in the exception list.
    Go through each agreement in the agreement dictionary and then go
    through each exception in the exception list.
    Check if the user-selected exception matches.
    If it matches, then check is True.  This is a valid exception to the
    trade agreement, so the trade agreement does not apply.  So we
    set the exception to False in the agreement dictionary.

    Args:
        agreement ([dict]): Keys are trade agreements, values are dictionaries where the
            keys are form fields and the values are boolean.
        data ([dict]): Keys are form fields and values are the user inputted data.
        exception ([dict]): Keys are the exception names from the form fields and
            the values are the corresponding model name.
    
    Returns:
        [dict]: Returns the agreement dictionary now it has been updated with
            any instances where the exception_name is False.
    """
    for exception_name, model in exception.items():
        exception = data[exception_name]
        if exception:
            for k in agreement.keys():
                for ex in exception:
                    check = model.objects.filter(name=ex).values_list(k).get()[0]
                    if check:
                        agreement[k][exception_name] = False
        else:
            pass
    return agreement

def code_rule(agreement, data_dict):
    """This function checks the commodity code in the data
    dictionary then sends the agreement dict, organization, and code
    to the relevant commodity type coverage function.  Then the data
    is sent to the org_code_exclusion function.

    Args:
        agreement ([dict]): Keys are trade agreements, values are dictionaries where the
            keys are form fields and the values are boolean.
        data ([dict]): Keys are form fields and values are the user inputted data.

    Returns:
        [dict]: Returns the agreement dictionary now it has been updated with
            any instances where 'code' is False.
    """
    code = data_dict['code']
    commodity = data_dict['type']
    org = data_dict['entities']

    if str(commodity) == 'Goods':
        agreement = goods_coverage(agreement, org, code)
    elif str(commodity) == 'Services':
        agreement = services_coverage(agreement, code)
    else:
        agreement = construction_coverage(agreement, org, code)
    agreement = code_org_exclusion(agreement, org, code)
    return agreement

def determine_final_coverage(_agreement):
    """This takes the agreement dictionary which contains trade
    agreements as keys and values as dictionaries.  These nested dicts
    have a key for each form field and a boolean value for each value.

    For a trade agreement to apply all the form field values in the 
    nested dict must be true.

    This goes through each trade agreement, if all values in the nest dict
    is true then the key is the trade agreement and the value is set to True.  
    
    If not all form fields are true then it sets the agreement as key and
    sets the value as False.

    Args:
        _agreement ([dict]): Keys are trade agreements, values are dictionaries where the
            keys are form fields and the values are boolean.
    Returns:
        [dict]: A dict with keys for each trade agreement and a boolean value
        indicating whether the trade agreement applies (True) or does not apply (False).
    """
    cxt={k:True if all(_agreement[k].values()) else False for k in _agreement.keys()}
    return cxt

def get_coverage(data_dict):
    """This calls the functions for each trade agreement rule and then builds
    a dictionary to be used as a context dict in the output page.

    Args:
        data_dict ([dict]): Every key is a form field and every value is the user-selected value.

    Returns:
        [dict]: Original data_dict which has been updated to include the agreement_dict and
        final trade coverage.  These will be used for context when rendering the last page.
    """
    agreement_dict = create_agreement_dict()
    #Rules for different form fields
    agreement_dict = value_threshold_rule(agreement_dict, data_dict)
    agreement_dict = organization_rule(agreement_dict, data_dict)
    agreement_dict = code_rule(agreement_dict, data_dict)

    exception_dict = {
        'exceptions': GeneralException,
        'cfta_exceptions': CftaException,
    }
    agreement_dict = exceptions_rule(agreement_dict, data_dict, exception_dict)
    
    #At this point the functions only set False if the trade agreement did not apply.
    #If not false it is true, set true here.
    fields = ['code', 'entities', 'estimated_value', 'exceptions', 'cfta_exceptions']
    for f in fields:
        agreement_dict = set_true(agreement_dict, f)

    data_dict['ta'] = agreement_dict
    data_dict['bool'] = determine_final_coverage(agreement_dict)
    return data_dict

def get_ta_text(_ta_text):
    """At the top of the results page there is a sentence listing
    which trade agreements apply.  This function takes in the data_dict
    and add a key called 'output' that has the above mentioned sentence.

    Args:
        _ta_text ([dict]): This is the data_dictionary which also
        include the agreement dictionary and the final coverage dictionaries

    Returns:
        [dict]: The dictionary used as Args updated to include 'output'
    """
    if sum(_ta_text['bool'].values()) == 0:
        output = 'No trade agreements apply.  '
    else:
        output = ''
        for k, v in _ta_text['bool'].items():
            if v is True:
                output = output + k.upper() + ', '
    _ta_text['output'] = output[:-2]
    return _ta_text

def get_summary_text(_sum_text):
    """The results page has a summary of user input. 
    This function takes in the data_dict and removes
    and empty optional selections with lists of None.
    This returns the updated dictionary.

    Args:
        _sum_text ([dict]): Data dictionary that also include
        agreement dictionary, final trade coverage, and output text

    Returns:
        [dict]: The dictionary that was used as Arg but some fields updated.
    """
    _sum_text2 = {k:['None'] if not v else v for k,v in _sum_text.items()}
    if 'limited_tendering' in _sum_text2:
        pass
    else:
        _sum_text2['limited_tendering'] = ['None']
    return _sum_text2

def get_tables_text(_table_text):
    """The resuls page contains a table for each agreement which
    summarizes how the user-selected values determined whether
    that particular trade agreement is covered or not.

    This function takes in the data dict and prepares the text
    for those tables.

    Args:
        _table_text ([dict]): data dictionary containing the agreement
        dict, final trade agreements, output text, and summary text.

    Returns:
        [dict]: Returns the same dict as in Args but updated with table text.
    """
    _table_text['tables'] = {}
    for k1, v1 in _table_text['ta'].items():
        k1 = k1.upper()
        _table_text['tables'][k1] = {}
        for k2, v2 in v1.items():
            if k2 == 'type' or k2 == 'limited_tendering':
                pass
            else:
                k2 = k2.replace('_', ' ')
                k2 = k2.title()
                if k1 == 'CFTA':
                    k2 = k2.replace('Cfta Exceptions', 'CFTA Exceptions')
                    _table_text['tables'][k1][k2] = v2
                else:
                    if k2 == 'Cfta Exceptions':
                        pass
                    else:
                        _table_text['tables'][k1][k2] = v2
    return _table_text

def get_output_text(_output_text):
    """This function takes in a data dict and passes it through
    the three functions used to create user-friendly text.

    Args:
        _output_text ([dict]): This is a dict that contains, the data,
        agreements, final coverage.
    """
    _output_text = get_ta_text(_output_text)
    _output_text = get_summary_text(_output_text)
    _output_text = get_tables_text(_output_text)
    return _output_text


class OpenPDF(View):
    """On the results page there is a button a user can press to
    bring up the same page as a PDF.  This class builds the pdf.

    Args:
        View ([class]): Generic View
    """
    def get(self, request, *args, **kwargs):
        """When a user clicks on the button it gets the output of this function.

        Args:
            request ([object]): request objects
        """
        def render_to_pdf(template_src, context_dict={}):
            """This functions transforms the View into a pdf document.

            Args:
                template_src ([.html]): html template for the pdf
                context_dict (dict, optional): context dict for the output in the pdf.
                    Defaults to {}.

            Returns:
                [object]: HttpResponse object.
            """
            template = get_template(template_src)
            html  = template.render(context_dict)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
            return None

        _data_dict = {}
        _data_dict.update(self.request.session)
        _data_dict = get_coverage(_data_dict)
        _data_dict = get_output_text(_data_dict)
        pdf = render_to_pdf('pdf.html', _data_dict)
        return HttpResponse(pdf, content_type='application/pdf')


class CodeAutocomplete(autocomplete.Select2QuerySetView):
    """This is for the autocomplete commodity code field in the 
    mandatory elements page

    Args:
        autocomplete ([class]): View for the autocomplete
    """
    def get_queryset(self):
        """Returns different querysets depending on the user input
        in the Commodity Type field and any search input.

        Returns:
            [object]: Queryset filtered by commodity type and user text.
        """
        forward_type = self.forwarded.get('type', None)
        qs = Code.objects.all()
        if forward_type:
            value = CommodityType.objects.filter(id=forward_type).values_list('commodity_type_en').get()[0]

            qs = Code.objects.filter(type=value).all()
            if self.q:
                qs = Code.objects.filter(type=value).filter(code__icontains=self.q)
        return qs
    
    
class EntitiesAutocomplete(autocomplete.Select2QuerySetView):
    """Autocomplete field for the entities field in the 
    mandatory elements page.

    Args:
        autocomplete ([class]): Autocomplete View
    """
    def get_queryset(self):
        """Returns the queryset of entities filterd by any user inputted text.

        Returns:
            [object]: Queryset
        """
        qs = Organization.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class TypeAutocomplete(autocomplete.Select2QuerySetView):
    """Returns the queryset of commodity types filtered by any user inputted text.

    Args:
        autocomplete ([class]): Autocomplete View
    """
    def get_queryset(self):
        """Returns the queryset of commodity types filtered by user input

        Returns:
            [object]: queryset
        """
        qs = CommodityType.objects.all()

        if self.q:
            qs = qs.filter(commodity_type__icontains=self.q)
        
        return qs

def lt_condition(wizard):
    """The limited tendering page is only displayed if
    a trade agreement applies. This takes in the user inputted data
    from the form wizard.

    Args:
        wizard ([object]): Wizard object

    Returns:
        [bool]: True if a trade agreement
    applies and False if no trade agreement applies
    """
    lt_list = [f[0] for f in FORMS[:3]]

    data_dict = {}
    try:
        for f in lt_list:
            data_dict.update(wizard.get_cleaned_data_for_step(f))
    except:
        return True
    
    data_dict = get_coverage(data_dict)
    
    if sum(data_dict['bool'].values()) == 0:
        return False
    return True


class TradeForm(NamedUrlCookieWizardView):
    """This is the wizard view for the trade agreement form.

    Args:
        NamedUrlCookieWizardView ([class]): View

    Returns:
        [clas]: Returns a view of each form page or done page.
    """
    form_list = [f[1] for f in FORMS]
    url_name=url_name
    done_step_name=done_step_name

    def get_template_names(self):
        """Get the template names for each view.

        Returns:
            [list]: list of template names
        """
        form = [TEMPLATES[self.steps.current]]
        return form

    def get_form(self, step=None, data=None, files=None):
        """We super() this function to conditionally render
        the limited tendering field.

        Args:
            step ([str], optional): Str for current step name. Defaults to None.
            data ([dict], optional): Data dict. Defaults to None.
            files ([object], optional): Files. Defaults to None.

        Returns:
            [object]: form
        """
        form = super(TradeForm, self).get_form(step, data, files)
        
        if 'limited_tendering' in form.fields:
            lt_list = [f[0] for f in FORMS[:3]]
            data_dict = create_data_dict(self, lt_list)
            
            data_dict = get_coverage(data_dict)

            ta_applies = [k for k,v in data_dict['bool'].items() if v is True]

            query_list = []
            if ta_applies:
                qs = LimitedTenderingReason.objects.all()
                for ta in ta_applies:
                    field_name = ta
                    qs = qs.filter(**{field_name: True}).values_list('name')
                qs = [q[0] for q in qs]
                for q in qs:
                    query_list.append(q)
            form.fields['limited_tendering'].queryset = LimitedTenderingReason.objects.filter(name__in=query_list).only('name')
            
        return form

    def done(self, form_list, form_dict, **kwargs):
        """Renders the last page with the results

        Args:
            form_list ([list]): List of forms
            form_dict ([dict]): dict of forms

        Returns:
            [object]: Render object
        """
        #These three lines get us most of the way there.
        done_list = [f[0] for f in FORMS]
        data_dict = create_data_dict(self, done_list)
        data_dict = get_coverage(data_dict)

       
        def add_session_list(name, model):
            """Puts data into session, this is required for pdf page to 
            get access to the data.

            Args:
                name ([str]): field name
                model ([class]): Model class for the field name
            """
            ex_list = []
            v = data_dict[name]
            for ex in v:
                if ex != 'None':
                    check = model.objects.filter(name=ex).values_list('name').get()[0]
                else:
                    check = 'None'
                ex_list.append(check)
            self.request.session[name] = ex_list

        #This part puts the exceptions in session
        exception_dict = {
            'exceptions': GeneralException,
            'cfta_exceptions': CftaException
        }
        for k, v in exception_dict.items():
            add_session_list(k, v)
        if 'limited_tendering' in data_dict.keys():
            add_session_list('limited_tendering', LimitedTenderingReason)
        #Then put the data form fields in session
        data_fields = ['entities', 'estimated_value', 'type', 'code']
        for field in data_fields:
            self.request.session[field] = str(data_dict[field])

        #From the data_dict get the user-friendly text
        data_dict = get_output_text(data_dict)
        return render(self.request, 'done.html', data_dict)
