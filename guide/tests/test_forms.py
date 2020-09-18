from django.test import TestCase
from django.urls import reverse

from guide.forms import (CftaExceptionForm, GeneralExceptionForm,
                         LimitedTenderingForm, RequiredFieldsForm,
                         cfta_exceptions_label, code_label, entities_label,
                         estimated_value_error, estimated_value_label,
                         general_exceptions_label, generic_error,
                         limited_tendering_label, type_label)
from guide.models import (CftaException, Code, CodeOrganizationExclusion,
                          CommodityType, ConstructionCoverage,
                          GeneralException, GoodsCoverage,
                          LimitedTenderingReason, Organization, ValueThreshold)


class FormsTest(TestCase):
    urls = 'django.contrib.formtools.tests.wizard.wizardtests.urls'


    @classmethod
    def setUpTestData(cls):
        Organization.objects.create(name='Model Ministry')
        CommodityType.objects.create(commodity_type='Model Commodity Type')
        Code.objects.create(code='ZZZ Model Commodity Code', type=CommodityType.objects.get(id=1))
        ValueThreshold.objects.create(type=CommodityType.objects.get(id=1))
        LimitedTenderingReason.objects.create(name='Model Limited Tendering Reason')
        GeneralException.objects.create(name='Model General Exception')
        CftaException.objects.create(name='Model CFTA Exception')
        GoodsCoverage.objects.create(org_fk=Organization.objects.get(id=1))
        ConstructionCoverage.objects.create(org_fk=Organization.objects.get(id=1))
        CodeOrganizationExclusion.objects.create(code_fk=Code.objects.get(id=1), org_fk=Organization.objects.get(id=1))

    def test_required_fields_labels(self):
        form = RequiredFieldsForm()
        self.assertIn(str(estimated_value_label), form.as_p())
        self.assertIn(str(entities_label), form.as_p())
        self.assertIn(str(type_label), form.as_p())
        self.assertIn(str(code_label), form.as_p())

    def test_general_exceptions_label(self):
        form = GeneralExceptionForm()
        self.assertIn(str(general_exceptions_label), form.as_p())
        
    def test_cfta_exceptions_label(self):
        form = CftaExceptionForm()
        self.assertIn(str(cfta_exceptions_label), form.as_p())
    
    def test_limited_tendering_label(self):
        form = LimitedTenderingForm()
        self.assertIn(str(limited_tendering_label), form.as_p())

    def test_required_fields_estimated_value_valid(self):
        form = RequiredFieldsForm({'estimated_value': 1000, 'entities': Organization.objects.get(id=1), 'type': CommodityType.objects.get(id=1), 'code': Code.objects.get(id=1)})
        form.is_valid()
        self.assertEqual(1000, form.cleaned_data['estimated_value'])

    def test_required_fields_entities_valid(self):
        form = RequiredFieldsForm({'estimated_value': 1000, 'entities': Organization.objects.get(id=1), 'type': CommodityType.objects.get(id=1), 'code': Code.objects.get(id=1)})
        form.is_valid()
        self.assertEqual(Organization.objects.get(id=1), form.data['entities'])

    def test_required_fields_type_valid(self):
        form = RequiredFieldsForm({'estimated_value': 1000, 'entities': Organization.objects.get(id=1), 'type': CommodityType.objects.get(id=1), 'code': Code.objects.get(id=1)})
        form.is_valid()
        self.assertEqual(CommodityType.objects.get(id=1), form.data['type'])



    def test_required_fields_blank(self):
        form = RequiredFieldsForm(data={'estimated_value': None, 'entities': None, 'type': None, 'code': None})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['estimated_value'], ['This field is required.'])
        self.assertEqual(form.errors['entities'], ['This field is required.'])
        self.assertEqual(form.errors['type'], ['This field is required.'])
        self.assertEqual(form.errors['code'], [generic_error])

    def test_required_fields_wrong_data_one(self):
        form = RequiredFieldsForm(data={'estimated_value': -1676, 'entities': 'Missing dept', 'type': 'missing type', 'code': 'missing code'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['estimated_value'], ['Ensure this value is greater than or equal to 0.'])
        self.assertEqual(form.errors['entities'], [generic_error])
        self.assertEqual(form.errors['type'], [generic_error])
        self.assertEqual(form.errors['code'], [generic_error])

    def test_required_fields_wrong_data_two(self):
        form = RequiredFieldsForm(data={'estimated_value': 'dsfdsf', 'entities': 'Missing dept', 'type': 'missing type', 'code': 'missing code'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['estimated_value'], ['Enter a whole number.'])
        self.assertEqual(form.errors['entities'], [generic_error])
        self.assertEqual(form.errors['type'], [generic_error])
        self.assertEqual(form.errors['code'], [generic_error])

    def test_general_exceptions_blank(self):
        form = GeneralExceptionForm(data={'exceptions': ''})
        self.assertTrue(form.is_valid())

    def test_general_exceptions_wrong(self):
        form = GeneralExceptionForm(data={'exceptions': ['missing exception']})
        self.assertFalse(form.is_valid())

    def test_general_exceptions_valid(self):
        form = GeneralExceptionForm(data={'exceptions': [GeneralException.objects.get(id=1)]})
        self.assertTrue(form.is_valid())

    def test_cfta_exceptions_blank(self):
        form = CftaExceptionForm(data={'cfta_exceptions': ''})
        self.assertTrue(form.is_valid())
    
    def test_cfta_exceptions_wrong(self):
        form = CftaExceptionForm(data={'cfta_exceptions': ['missing exception']})
        self.assertFalse(form.is_valid())
    
    def test_cfta_exceptions_valid(self):
        form = CftaExceptionForm(data={'cfta_exceptions': [CftaException.objects.get(id=1)]})
        self.assertTrue(form.is_valid())

    def test_limited_tendering_blank(self):
        form = LimitedTenderingForm(data={'limited_tendering': ''})
        self.assertTrue(form.is_valid())
    
    def test_limited_tendering_wrong(self):
        form = LimitedTenderingForm(data={'limited_tendering': 'missing reason'})
        self.assertFalse(form.is_valid())
    
    def test_limited_tendering_valid(self):
        form = LimitedTenderingForm(data={'limited_tendering': [LimitedTenderingReason.objects.get(id=1)]})
        self.assertTrue(form.is_valid())
