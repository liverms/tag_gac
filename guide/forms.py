from django import forms
from django.forms.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from guide.models import Entities, Code, TAException, TenderingReason, CftaException
from django.db.models import Q


class GuideFormEN(forms.Form):
    estimated_value = forms.IntegerField(
        label=_('Estimated Value'),
        required=True
    )
    estimated_value.widget.attrs['class'] = 'form-control required'

    entities = forms.ModelChoiceField(
        Entities.objects.filter(Q(lang='EN') | Q(lang='BI')).only('name'),
        label=_('Organization'),
        required=True
    )
    entities.widget.attrs['class'] = 'form-control'

    commodity_type = forms.ModelChoiceField(
        Code.objects.filter(Q(lang='EN') | Q(lang='BI')).only('type'),
        label=_('Commodity Type'),
        required=True
    )
    commodity_type.widget.attrs['class'] = 'form-control'


    commodity_system = forms.ModelChoiceField(
        Code.objects.filter(Q(lang='EN') | Q(lang='BI')).only('code_system'),
        label=_('Commodity Code System'),
        required=True
    )
    commodity_system.widget.attrs['class'] = 'form-control'


    commodity_code = forms.ModelChoiceField(
        Code.objects.filter(Q(lang='EN') | Q(lang='BI')).only('code'),
        label=_('Commodity Code'),
        required=True
    )
    commodity_code.widget.attrs['class'] = 'form-control'



    exceptions = forms.ModelMultipleChoiceField(
        TAException.objects.filter(Q(lang='EN') | Q(lang='BI')).only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Exceptions"),
        required=False
    )
    exceptions.widget.attrs['class'] = 'form-control'


    limited_tendering = forms.ModelMultipleChoiceField(
        TenderingReason.objects.filter(Q(lang='EN') | Q(lang='BI')).only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Limited Tendering Reasons"),
        required=False
    )
    limited_tendering.widget.attrs['class'] = 'form-control'

    cfta_exceptions = forms.ModelMultipleChoiceField(
        CftaException.objects.filter(Q(lang='EN') | Q(lang='BI')).only('name'),
        to_field_name='id',
        widget=forms.CheckboxSelectMultiple,
        label=_("CFTA Exceptions"),
        required=False
    )
    cfta_exceptions.widget.attrs['class'] = 'form-control'

class GuideFormFR(forms.Form):
    estimated_value = forms.IntegerField(
        label=_('Estimated Value'),
        required=True
    )
    estimated_value.widget.attrs['class'] = 'form-control required'

    entities = forms.ModelChoiceField(
        Entities.objects.filter(Q(lang='FR') | Q(lang='BI')).only('name'),
        label=_('Organization'),
        required=True
    )
    entities.widget.attrs['class'] = 'form-control'

    commodity_type = forms.ModelChoiceField(
        Code.objects.filter(Q(lang='FR') | Q(lang='BI')).only('type'),
        label=_('Commodity Type'),
        required=True
    )
    commodity_type.widget.attrs['class'] = 'form-control'

    commodity_system = forms.ModelChoiceField(
        Code.objects.filter(Q(lang='FR') | Q(lang='BI')).only('code_system'),
        label=_('Commodity Code System'),
        required=True
    )
    commodity_system.widget.attrs['class'] = 'form-control'

    commodity_code = forms.ModelChoiceField(
        Code.objects.filter(Q(lang='FR') | Q(lang='BI')).only('code'),
        label=_('Commodity Code'),
        required=True
    )
    commodity_type.widget.attrs['class'] = 'form-control'

    exceptions = forms.ModelMultipleChoiceField(
        TAException.objects.filter(Q(lang='FR') | Q(lang='BI')).only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Exceptions"),
        required=False
    )
    exceptions.widget.attrs['class'] = 'form-control'

    limited_tendering = forms.ModelMultipleChoiceField(
        TenderingReason.objects.filter(Q(lang='FR') | Q(lang='BI')).only('name'),
        widget=forms.CheckboxSelectMultiple,
        label=_("Limited Tendering Reasons"),
        required=False
    )
    limited_tendering.widget.attrs['class'] = 'form-control'

    cfta_exceptions = forms.ModelMultipleChoiceField(
        CftaException.objects.filter(Q(lang='FR') | Q(lang='BI')).only('name'),
        to_field_name='id',
        widget=forms.CheckboxSelectMultiple,
        label=_("CFTA Exceptions"),
        required=False
    )
    cfta_exceptions.widget.attrs['class'] = 'form-control'

    # def clean_commodity_type(self):
    #     '''
    #     Provide a custom validation for the commodity type select field. Whatever commodity type is selected the
    #     corresponding goods, services, or construction select field must have a selected item.
    #     :return: A ValidationError if the corresponding commodity is not selected.
    #     '''
    #     if self.cleaned_data['commodity_type'] == 'goods':
    #         if 'goods_codes' not in self.data or self.data['goods_codes'] is None:
    #             raise ValidationError(
    #                 _('Select a good from the list below'),
    #                 code='invalid',
    #             )
    #         try:
    #             code = int(self.data['goods_codes'])
    #         except:
    #             raise ValidationError(
    #                 _('Select a good from the list below'),
    #                 code='invalid',
    #             )
    #     elif self.cleaned_data['commodity_type'] == 'services':
    #         if 'services_codes' not in self.data or self.data['services_codes'] is None:
    #             raise ValidationError(
    #                 _('Select a service from the list below'),
    #                 code='invalid',
    #             )
    #         try:
    #             code = int(self.data['services_codes'])
    #         except:
    #             raise ValidationError(
    #                 _('Select a service from the list below'),
    #                 code='invalid',
    #             )
    #     elif self.cleaned_data['commodity_type'] == 'construction':
    #         if 'construction_code' not in self.data or self.data['construction_code'] is None:
    #             raise ValidationError(
    #                 _('Select a construction from the list below'),
    #                 code='invalid',
    #             )
    #         try:
    #             code = int(self.data['construction_code'])
    #         except:
    #             raise ValidationError(
    #                 _('Select a construction from the list below'),
    #                 code='invalid',
    #             )
