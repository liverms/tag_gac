from dal import autocomplete
from django import forms
from django.forms.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from guide.models import (
    CftaException, Code, CommodityType, GeneralException,
    LimitedTenderingReason, Organization)

estimated_value_label = _('What is the total estimated value of the procurement? ')
entities_label = _('Who is the procuring entity?')
type_label = _('What is the procurement commodity type?')
code_label = _('What is the Goods and Services Identification Number commodity (GSIN) code most closely associated with the procurement?')
general_exceptions_label = _("Exceptions")
limited_tendering_label = _("Limited Tendering Reasons")
cfta_exceptions_label = _("CFTA Exceptions")

estimated_value_error = 'Please enter a valid number greater than zero.'
generic_error = 'Select a valid choice. That choice is not one of the available choices.'


class RequiredFieldsForm(forms.Form):
    """All the fields in this form are required.
    However, for the code field required is set to False.
    Also, for the template this is associated with novalidate 
    is specified.

    This is because it was difficult to stop the client-side
    validation the GC uses for autocomplete fields.  This is because
    when the page first renders this field is empty. Instead this
    relies on the use of a clean method for this field to ensure
    the user has input the correct information.

    The autocomplete fields rely on a View and a url to work.
    The url is specified in the widget.

    Args:
        forms ([class]): Form Class

    Returns:
        [class]: Returns form with the fields below.
    """
    estimated_value = forms.IntegerField(
        label = estimated_value_label,
        required = True,
        min_value = 0
    )
    estimated_value.widget.attrs['class'] = 'form-control'

    entities = forms.ModelChoiceField(
        Organization.objects.all(),
        label = entities_label,
        required = True,
        widget=autocomplete.ModelSelect2(
            url='guide:entities_autocomplete', 
            attrs={'class':'form-control'}
        )
    )

    type = forms.ModelChoiceField(
        CommodityType.objects.all(),
        label = type_label,
        required = True,
        widget = autocomplete.ModelSelect2(
            url='guide:type_autocomplete', 
            attrs={'class':'form-control'}
            )
    )

    code = forms.ModelChoiceField(
        Code.objects.only('code').all(),
        label = code_label,
        required = False,
        widget = autocomplete.ModelSelect2(
            url = 'guide:code_autocomplete', 
            forward=['type'], 
            attrs={'class':'form-control', 'size': '1'}
        )
    )

    def clean_code(self):
        """Clean the code field for validation after
        the user submits the form.

        Raises:
            ValidationError: Raise warning to user
            to select valid Commodity Code

        Returns:
            [str]: Str of user-selected code
        """
        code = self.cleaned_data['code']
        if Code.objects.filter(code = code).exists():
            return code
        else:
            raise ValidationError(generic_error)


class GeneralExceptionForm(forms.Form):
    """Form for general exceptions.

    Args:
        forms ([class]): Form class
    """
    exceptions = forms.ModelMultipleChoiceField(
        GeneralException.objects.only('name'),
        to_field_name = 'id',
        widget = forms.CheckboxSelectMultiple,
        label = general_exceptions_label,
        required = False
    )
    exceptions.widget.attrs['class'] = 'form-control'


class LimitedTenderingForm(forms.Form):
    """Limited Tendering Form

    Args:
        forms ([class]): Form class
    """
    limited_tendering = forms.ModelMultipleChoiceField(
        LimitedTenderingReason.objects.only('name'),
        to_field_name = 'id',
        widget = forms.CheckboxSelectMultiple,
        label = limited_tendering_label,
        required = False
    )
    limited_tendering.widget.attrs['class'] = 'form-control'


class CftaExceptionForm(forms.Form):
    """CFTA form

    Args:
        forms ([class]): Form class
    """
    cfta_exceptions = forms.ModelMultipleChoiceField(
        CftaException.objects.only('name'),
        to_field_name = 'id',
        widget = forms.CheckboxSelectMultiple,
        label = cfta_exceptions_label,
        required = False
    )
