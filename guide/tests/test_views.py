import unittest

from django.test import TestCase

from guide.forms import (CftaExceptionForm, GeneralExceptionForm,
                         LimitedTenderingForm, RequiredFieldsForm)
from guide.models import (AGREEMENTS_FIELDS, CftaException, Code,
                          CodeOrganizationExclusion, CommodityType,
                          ConstructionCoverage, GeneralException,
                          GoodsCoverage, LimitedTenderingReason, Organization,
                          ValueThreshold)
from guide.views import (FORMS, CodeAutocomplete, EntitiesAutocomplete,
                         OpenPDF, TradeForm, TypeAutocomplete,
                         code_org_exclusion, code_rule, construction_coverage,
                         create_agreement_dict, determine_final_coverage,
                         exceptions_rule, get_coverage, get_output_text,
                         goods_coverage, lt_condition, organization_rule,
                         services_coverage, set_code_false,
                         set_exception_false, set_true, value_threshold_rule)


class ViewTests(TestCase):
    # fixtures = ['db.json']
    @classmethod
    def setUpTestData(cls):
        Organization.objects.create(
            id=1,
            name='Model Ministry',
            name_fr='Model Ministry FR',
            ccfta = True, 
            ccofta = True, 
            chfta = True, 
            cpafta = True, 
            cpfta = True, 
            ckfta = False, 
            cufta = False, 
            wto_agp = False, 
            ceta = False, 
            cptpp = False, 
            cfta = False
            )
        Organization.objects.create(
            id=2,
            name='Construction Ministry',
            name_fr='Construction Ministry Fr',
            ccfta = True, 
            ccofta = True, 
            chfta = True, 
            cpafta = True, 
            cpfta = True, 
            ckfta = False, 
            cufta = False, 
            wto_agp = False, 
            ceta = False, 
            cptpp = False, 
            cfta = False
        )
        Organization.objects.create(
            id=3,
            name='Goods Ministry',
            name_fr='Goods Ministry Fr',
            ccfta = True, 
            ccofta = True, 
            chfta = True, 
            cpafta = True, 
            cpfta = True, 
            ckfta = False, 
            cufta = False, 
            wto_agp = False, 
            ceta = False, 
            cptpp = False, 
            cfta = False
        )
        CommodityType.objects.create(c_type='1', commodity_type='Goods', commodity_type_fr='Produits')
        CommodityType.objects.create(c_type='2', commodity_type='Services', commodity_type_fr='Services')
        CommodityType.objects.create(c_type='3', commodity_type='Construction', commodity_type_fr='Construction')
        Code.objects.create(
            code='Goods Commodity Code',
            code_fr = 'Goods Commodity Code FR',
            type=CommodityType.objects.get(id=1),
            ccfta = True, 
            ccofta = True, 
            chfta = True, 
            cpafta = True, 
            cpfta = True, 
            ckfta = False, 
            cufta = False, 
            wto_agp = False, 
            ceta = False, 
            cptpp = False, 
            cfta = False
        )
        Code.objects.create(
            code='All Commodity Codes Apply', 
            code_fr = 'All Commodity Code FR',
            type=CommodityType.objects.get(id=2),
            ccfta = True, 
            ccofta = True, 
            chfta = True, 
            cpafta = True, 
            cpfta = True, 
            ckfta = True, 
            cufta = True, 
            wto_agp = True, 
            ceta = True, 
            cptpp = True, 
            cfta = True
        )
        ValueThreshold.objects.create(
            type=CommodityType.objects.get(id=1), 
            ccfta = 10000, 
            ccofta = 10000, 
            chfta = 10000, 
            cpafta = 10000, 
            cpfta = 10000, 
            ckfta = 10000, 
            cufta = 10000, 
            wto_agp = 10000, 
            ceta = 10000, 
            cptpp = 10000, 
            cfta = 10000
            )
        LimitedTenderingReason.objects.create(name='Model Limited Tendering Reason')
        GeneralException.objects.create(
            name='Model General Exception',
            name_fr='Model General Exception FR',
            ccfta = True, 
            ccofta = True, 
            chfta = True, 
            cpafta = True, 
            cpfta = True, 
            ckfta = False, 
            cufta = False, 
            wto_agp = False, 
            ceta = False, 
            cptpp = False, 
            cfta = False
            )
        CftaException.objects.create(
            name='Model CFTA Exception',
            ccfta = False, 
            ccofta = False, 
            chfta = False, 
            cpafta = False, 
            cpfta = False, 
            ckfta = False, 
            cufta = False, 
            wto_agp = False, 
            ceta = False, 
            cptpp = False, 
            cfta = True
        )
        GoodsCoverage.objects.create(
            org_fk=Organization.objects.get(id=3)
            )
        ConstructionCoverage.objects.create(
            org_fk=Organization.objects.get(id=2),
            ccfta = True, 
            ccofta = True, 
            chfta = True, 
            cpafta = True, 
            cpfta = True, 
            ckfta = False, 
            cufta = False, 
            wto_agp = False, 
            ceta = False, 
            cptpp = False, 
            cfta = False
        )
        CodeOrganizationExclusion.objects.create(
            code_fk=Code.objects.get(id=2),
            org_fk=Organization.objects.get(id=1),
            ccfta = True, 
            ccofta = True, 
            chfta = True, 
            cpafta = True, 
            cpfta = True, 
            ckfta = False, 
            cufta = False, 
            wto_agp = False, 
            ceta = False, 
            cptpp = False, 
            cfta = False
            )

    def test_create_data_dict(self):
        #Cant validate forms
        pass

    def test_create_agreement_dict(self):
        test_dict = create_agreement_dict()

        mock_dict = {
            'ccfta': {},
            'ccofta': {},
            'chfta': {},
            'cpafta': {},
            'cpfta': {},
            'ckfta': {},
            'cufta': {},
            'wto_agp': {},
            'ceta': {},
            'cptpp': {},
            'cfta': {}
        }

        self.assertEqual(test_dict, mock_dict)
        self.assertTrue(test_dict == mock_dict)
        self.assertFalse(test_dict != mock_dict)

    def test_value_threshold_rule_false(self):
        aggreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 10,
            'entities': Organization.objects.get(id=1),
            'type': 'Goods',
            'code': Code.objects.get(id=1),
            'exceptions': GeneralException.objects.get(id=1),
            'limited_tendering': LimitedTenderingReason.objects.get(id=1),
            'cfta_exceptions': CftaException.objects.get(id=1)
        }

        agreement = value_threshold_rule(aggreement_dict, mock_data)
        false_dict = {'estimated_value': False}
        empty_dict = {}
        true_dict = {'estimated_value': True}
        for v in agreement.values():
            self.assertEqual(false_dict, v)
            self.assertTrue(false_dict == v)
            self.assertFalse(false_dict != v)
            self.assertFalse(empty_dict == v)
            self.assertFalse(true_dict == v)

    def test_value_threshold_rule_true(self):
        aggreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 100000,
            'entities': Organization.objects.get(id=1),
            'type': 'Goods',
            'code': Code.objects.get(id=1),
            'exceptions': GeneralException.objects.get(id=1),
            'limited_tendering': LimitedTenderingReason.objects.get(id=1),
            'cfta_exceptions': CftaException.objects.get(id=1)
        }

        agreement = value_threshold_rule(aggreement_dict, mock_data)
        false_dict = {'estimated_value': False}
        empty_dict = {}
        true_dict = {'estimated_value': True}
        for v in agreement.values():
            self.assertEqual(empty_dict, v)
            self.assertTrue(empty_dict == v)
            self.assertFalse(empty_dict != v)
            self.assertFalse(false_dict == v)
            self.assertFalse(true_dict == v)

    def test_organization_rule(self):
        aggreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 100000,
            'entities': Organization.objects.get(id=1),
            'type': 'Goods',
            'code': Code.objects.get(id=1),
            'exceptions': GeneralException.objects.get(id=1),
            'limited_tendering': LimitedTenderingReason.objects.get(id=1),
            'cfta_exceptions': CftaException.objects.get(id=1)
        }

        agreement = organization_rule(aggreement_dict, mock_data)
        true_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta']
        false_aggreements = ['ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        false_dict = {'entities': False}
        empty_dict = {}
        true_dict = {'entities': True}

        for k, v in agreement.items():
            if k in true_aggreements:
                self.assertEqual(empty_dict, v)
                self.assertFalse(false_dict ==  v)
                self.assertFalse(true_dict ==  v)
            if k in false_aggreements:
                self.assertEqual(false_dict, v)
                self.assertFalse(empty_dict == v)
                self.assertFalse(true_dict == v)
            if (k not in true_aggreements) and (k not in false_aggreements):
                self.assertEqual(1, 2)

    
    def test_construction_coverage(self):
        aggreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 100000,
            'entities': 'Construction Ministry',
            'type': 'Construction',
            'code': Code.objects.get(id=1),
            'exceptions': GeneralException.objects.get(id=1),
            'limited_tendering': LimitedTenderingReason.objects.get(id=1),
            'cfta_exceptions': CftaException.objects.get(id=1)
        }

        agreement = construction_coverage(aggreement_dict, mock_data['type'], mock_data['entities'], mock_data['code'])
        true_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta']
        false_aggreements = ['ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        false_dict = {'code': False}
        empty_dict = {}
        true_dict = {'code': True}

        for k, v in agreement.items():
            if k in true_aggreements:
                self.assertEqual(false_dict, v)
                self.assertFalse(empty_dict == v)
                self.assertFalse(true_dict == v)
            if k in false_aggreements:
                self.assertEqual(empty_dict, v)
                self.assertFalse(false_dict ==  v)
                self.assertFalse(true_dict ==  v)
            if (k not in true_aggreements) and (k not in false_aggreements):
                self.assertEqual(1, 2)

    def test_goods_coverage(self):
        aggreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 100000,
            'entities': 'Goods Ministry',
            'type': 'Construction',
            'code': Code.objects.get(id=1),
            'exceptions': [GeneralException.objects.get(id=1)],
            'limited_tendering': LimitedTenderingReason.objects.get(id=1),
            'cfta_exceptions': CftaException.objects.get(id=1)
        }

        agreement = goods_coverage(aggreement_dict, mock_data['type'], mock_data['entities'], mock_data['code'])
        true_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta']
        false_aggreements = ['ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        false_dict = {'code': False}
        empty_dict = {}
        true_dict = {'code': True}

        for k, v in agreement.items():
            if k in true_aggreements:
                self.assertEqual(empty_dict, v)
                self.assertFalse(false_dict ==  v)
                self.assertFalse(true_dict ==  v)
            if k in false_aggreements:

                self.assertEqual(false_dict, v)
                self.assertFalse(empty_dict == v)
                self.assertFalse(true_dict == v)
            if (k not in true_aggreements) and (k not in false_aggreements):
                self.assertEqual(1, 2)

    def test_services_coverage(self):
        aggreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 100000,
            'entities': 'Goods Ministry',
            'type': 'Construction',
            'code': Code.objects.get(id=1),
            'exceptions': GeneralException.objects.get(id=1),
            'limited_tendering': LimitedTenderingReason.objects.get(id=1),
            'cfta_exceptions': CftaException.objects.get(id=1)
        }

        agreement = services_coverage(aggreement_dict, mock_data['type'], mock_data['entities'], mock_data['code'])
        true_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta']
        false_aggreements = ['ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        false_dict = {'code': False}
        empty_dict = {}
        true_dict = {'code': True}

        for k, v in agreement.items():
            if k in true_aggreements:
                self.assertEqual(empty_dict, v)
                self.assertFalse(false_dict ==  v)
                self.assertFalse(true_dict ==  v)
            if k in false_aggreements:

                self.assertEqual(false_dict, v)
                self.assertFalse(empty_dict == v)
                self.assertFalse(true_dict == v)
            if (k not in true_aggreements) and (k not in false_aggreements):
                self.assertEqual(1, 2)

    def test_code_org_exclusion(self):
        aggreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 100000,
            'entities': Organization.objects.get(id=1),
            'type': 'Construction',
            'code': Code.objects.get(id=2),
            'exceptions': GeneralException.objects.get(id=1),
            'limited_tendering': LimitedTenderingReason.objects.get(id=1),
            'cfta_exceptions': CftaException.objects.get(id=1)
        }

        agreement = code_org_exclusion(aggreement_dict, mock_data['type'], mock_data['entities'], mock_data['code'])
        true_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta']
        false_aggreements = ['ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        false_dict = {'code': False}
        empty_dict = {}
        true_dict = {'code': True}

        for k, v in agreement.items():
            if k in true_aggreements:
                self.assertEqual(false_dict, v)
                self.assertFalse(empty_dict == v)
                self.assertFalse(true_dict == v)
            if k in false_aggreements:
                self.assertEqual(empty_dict, v)
                self.assertFalse(false_dict ==  v)
                self.assertFalse(true_dict ==  v)
            if (k not in true_aggreements) and (k not in false_aggreements):
                self.assertEqual(1, 2)

    def test_set_exception_false(self):
        aggreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 100000,
            'entities': Organization.objects.get(id=1),
            'type': 'Construction',
            'code': Code.objects.get(id=2),
            'exceptions': [GeneralException.objects.get(id=1)],
            'limited_tendering': LimitedTenderingReason.objects.get(id=1),
            'cfta_exceptions': CftaException.objects.get(id=1)
        }

        agreement = set_exception_false(aggreement_dict, mock_data['exceptions'], GeneralException, 'exceptions')
        true_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta']
        false_aggreements = ['ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        false_dict = {'exceptions': False}
        empty_dict = {}
        true_dict = {'exceptions': True}

        for k, v in agreement.items():
            if k in true_aggreements:
                self.assertEqual(false_dict, v)
                self.assertFalse(empty_dict == v)
                self.assertFalse(true_dict == v)
            if k in false_aggreements:
                self.assertEqual(empty_dict, v)
                self.assertFalse(false_dict ==  v)
                self.assertFalse(true_dict ==  v)
            if (k not in true_aggreements) and (k not in false_aggreements):
                self.assertEqual(1, 2)

    def test_set_code_false(self):
        aggreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 100000,
            'entities': Organization.objects.get(id=3),
            'type': CommodityType.objects.get(id=2),
            'code': Code.objects.get(id=1),
            'exceptions': [GeneralException.objects.get(id=1)],
            'limited_tendering': None,
            'cfta_exceptions': None
        }

        agreement = set_code_false(aggreement_dict, mock_data['type'], mock_data['entities'], mock_data['code'])
        true_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta']
        false_aggreements = ['ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        false_dict = {'code': False}
        empty_dict = {}
        true_dict = {'code': True}

        for k, v in agreement.items():
            if k in true_aggreements:
                self.assertEqual(empty_dict, v)
                self.assertFalse(false_dict ==  v)
                self.assertFalse(true_dict ==  v)
            if k in false_aggreements:
                self.assertEqual(false_dict, v)
                self.assertFalse(empty_dict == v)
                self.assertFalse(true_dict == v)
            if (k not in true_aggreements) and (k not in false_aggreements):
                self.assertEqual(1, 2)

    def test_set_true_all_true(self):
        aggreement_dict = create_agreement_dict()

        agreement = set_true(aggreement_dict, 'code')
        true_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        false_dict = {'code': False}
        empty_dict = {}
        true_dict = {'code': True}

        for k, v in agreement.items():
            if k in true_aggreements:
                self.assertEqual(true_dict, v)
                self.assertFalse(false_dict ==  v)
                self.assertFalse(empty_dict ==  v)
            if (k not in true_aggreements):
                self.assertEqual(1, 2)

    def test_set_true_all_false(self):
        aggreement_dict = create_agreement_dict()
        false_dict = {'code': False}
        for k in aggreement_dict.keys():
            aggreement_dict[k].update(false_dict)
        agreement = set_true(aggreement_dict, 'code')
        false_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta', 'ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        empty_dict = {}
        true_dict = {'code': True}

        for k, v in agreement.items():
            if k in false_aggreements:
                self.assertEqual(false_dict, v)
                self.assertFalse(true_dict ==  v)
                self.assertFalse(empty_dict ==  v)
            if (k not in false_aggreements):
                self.assertEqual(1, 2)

    def test_exceptions_rule(self):
        aggreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 100000,
            'entities': Organization.objects.get(id=1),
            'type': 'Construction',
            'code': Code.objects.get(id=2),
            'exceptions': [GeneralException.objects.get(id=1)],
            'limited_tendering': LimitedTenderingReason.objects.get(id=1),
            'cfta_exceptions': [CftaException.objects.get(id=1)]
        }
        
        exception_dict = {
            'exceptions': GeneralException
        }

        agreement = exceptions_rule(aggreement_dict, mock_data, exception_dict)
        true_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta']
        false_aggreements = ['ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        false_dict = {'exceptions': False}
        empty_dict = {}
        true_dict = {'exceptions': True}

        for k, v in agreement.items():
            if k in true_aggreements:
                self.assertEqual(false_dict, v)
                self.assertFalse(empty_dict == v)
                self.assertFalse(true_dict == v)
            if k in false_aggreements:
                self.assertEqual(true_dict, v)
                self.assertFalse(false_dict ==  v)
                self.assertFalse(empty_dict ==  v)
            if (k not in true_aggreements) and (k not in false_aggreements):
                self.assertEqual(1, 2)

    def test_code_rule(self):
        aggreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 100000,
            'entities': Organization.objects.get(id=1),
            'type': 'Construction',
            'code': Code.objects.get(id=1),
            'exceptions': [GeneralException.objects.get(id=1)],
            'limited_tendering': LimitedTenderingReason.objects.get(id=1),
            'cfta_exceptions': [CftaException.objects.get(id=1)]
        }
        
        agreement = code_rule(aggreement_dict, mock_data)
        true_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta']
        false_aggreements = ['ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        false_dict = {'code': False}
        empty_dict = {}
        true_dict = {'code': True}

        for k, v in agreement.items():
            if k in true_aggreements:
                self.assertEqual(true_dict, v)
                self.assertFalse(false_dict ==  v)
                self.assertFalse(empty_dict ==  v)
            if k in false_aggreements:
                self.assertEqual(false_dict, v)
                self.assertFalse(empty_dict == v)
                self.assertFalse(true_dict == v)
            if (k not in true_aggreements) and (k not in false_aggreements):
                self.assertEqual(1, 2)

    def test_determine_final_coverage(self):
        agreement_dict = create_agreement_dict()

        mock_data = {
            'estimated_value': 100000,
            'entities': Organization.objects.get(id=1),
            'type': 'Construction',
            'code': Code.objects.get(id=1),
            'exceptions': None,
            'limited_tendering': [LimitedTenderingReason.objects.get(id=1)],
            'cfta_exceptions': None
        }
        
        agreement_dict = value_threshold_rule(agreement_dict, mock_data)
        agreement_dict = organization_rule(agreement_dict, mock_data)
        agreement_dict = code_rule(agreement_dict, mock_data)

        exception_dict = {
            'exceptions': GeneralException,
            'cfta_exceptions': CftaException,
        }
        agreement_dict = exceptions_rule(agreement_dict, mock_data, exception_dict)
        check = determine_final_coverage(agreement_dict)

        true_aggreements = ['ccfta', 'ccofta', 'chfta', 'cpafta', 'cpfta']
        false_aggreements = ['ckfta', 'cufta', 'wto_agp', 'ceta', 'cptpp', 'cfta']

        for k, v in check.items():
            if k in true_aggreements:
                self.assertEqual(True, v)
                self.assertFalse(False ==  v)
                self.assertFalse(None == v)
            if k in false_aggreements:
                self.assertEqual(False, v)
                self.assertFalse(None == v)
                self.assertFalse(True == v)
            if (k not in true_aggreements) and (k not in false_aggreements):
                self.assertEqual(1, 2)
# def determine_final_coverage(_agreement):
#     """[summary]

#     Args:
#         _agreement ([type]): [description]

#     Returns:
#         [type]: [description]
#     """
#     cxt={k:True if all(_agreement[k].values()) else False for k in _agreement.keys()}
#     return cxt
# for exception_name, model in exception.items():
#     exception = data[exception_name]
#     if exception:
#         agreement = set_exception_false(agreement, exception, model, exception_name)
#     agreement = set_exception_true(agreement, exception_name)
#     def test_build_context_dict(self):
#         cxt = build_context_dict()
#         self.assertIsInstance(cxt, dict)
#         for ta in AGREEMENTS:
#             self.assertIn(ta, cxt['ta'])
        
#     def add_data(self):

#         rf_data = {'estimated_value': 1000, 'entities': Organization.objects.get(id=1).pk, 'type': CommodityType.objects.get(id=1), 'code': Code.objects.get(id=1)}
#         ge_data = {'exceptions': [GeneralException.objects.get(id=1)]}
#         ce_data = {'cfta_exceptions': [CftaException.objects.get(id=1)]}
#         lt_data = {'limited_tendering': [LimitedTenderingReason.objects.get(id=1)]}

#         rf = RequiredFieldsForm(data=rf_data)
#         ge = GeneralExceptionForm(data=ge_data)
#         ce = CftaExceptionForm(data=ce_data)
#         lt = LimitedTenderingForm(data=lt_data)

#         rf.is_valid()
#         ge.is_valid()
#         ce.is_valid()
#         lt.is_valid()

#         return rf, ge, ce, lt

#     def test_process_form(self):
#         rf, ge, ce, lt = self.add_data()
#         cxt = build_context_dict()

#         all_data = {}
#         all_data.update(rf.cleaned_data)
#         all_data.update(ge.cleaned_data)
#         all_data.update(ce.cleaned_data)
#         all_data.update(lt.cleaned_data)

#         form_list = [rf, ge, ce, lt]
#         for form in form_list:
#             cxt = process_form(cxt, form.cleaned_data)

#         self.assertIsInstance(cxt, dict)
#         self.assertTrue(all_data.items() <= cxt.items())

#         for ta in AGREEMENTS:
#             self.assertTrue(all_data.keys() <= cxt['ta'][ta].keys())
#             self.assertNotIn(False, cxt['ta'][ta].values())
#             self.assertIn(True, cxt['ta'][ta].values())
#             for val in cxt['ta'][ta].values():
#                 self.assertTrue(val is True)
#             self.assertIn(ta, cxt['ta'])

#     def test_check_if_trade_agreement_applies(self):
#         cxt = build_context_dict()

#         rf_data = {'estimated_value': 1000, 'entities': Organization.objects.get(id=1).pk, 'type': CommodityType.objects.get(id=1), 'code': Code.objects.get(id=1)}
#         ge_data = {'exceptions': [GeneralException.objects.get(id=1)]}
#         ce_data = {'cfta_exceptions': [CftaException.objects.get(id=1)]}
#         lt_data = {'limited_tendering': [LimitedTenderingReason.objects.get(id=1)]}

#         rf = RequiredFieldsForm(data=rf_data)
#         ge = GeneralExceptionForm(data=ge_data)
#         ce = CftaExceptionForm(data=ce_data)
#         lt = LimitedTenderingForm(data=lt_data)

#         rf.is_valid()
#         ge.is_valid()
#         ce.is_valid()
#         lt.is_valid()

#         all_data = {}
#         all_data.update(rf.cleaned_data)
#         all_data.update(ge.cleaned_data)
#         all_data.update(ce.cleaned_data)
#         all_data.update(lt.cleaned_data)

#         form_list = [rf, ge, ce, lt]
#         for form in form_list:
#             cxt = process_form(cxt, form.cleaned_data)
            
#         code_name='code'
#         value = cxt[code_name]
#         data = Code.objects.filter(code=value)
#         for ta in cxt['ta']:
#             cxt = check_if_trade_agreement_applies(ta, cxt, data, code_name)

#         self.assertIsInstance(cxt, dict)
#         self.assertTrue(all_data.items() <= cxt.items())

# class TestViews(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         Organization.objects.create(name='Model Ministry')
#         CommodityType.objects.create(commodity_type='Model Commodity Type')
#         Code.objects.create(code='ZZZ Model Commodity Code', type=CommodityType.objects.get(id=1))
#         ValueThreshold.objects.create(type_value=CommodityType.objects.get(id=1))
#         LimitedTenderingReason.objects.create(name='Model Limited Tendering Reason')
#         GeneralException.objects.create(name='Model General Exception')
#         CftaException.objects.create(name='Model CFTA Exception')


#     wizard_urlname = url_name
#     wizard_step_1_data = {
#         'trade_wizard-current_step': '0',
#     }
#     wizard_step_data = (
#         {
#             'estimated_value': 1000,
#             'entities': 'Model Ministry',
#             'type': 'Model Commodity Type',
#             'code': 'ZZZ Model Commodity Code',
#             'trade_wizard-current_step': '0',
#         },
#         {
#             'exceptions': ['Model General Exception'],
#             'trade_wizard-current_step': '1',
#         },
#         {
#             'cfta_exceptions': ['Model CFTA Exception'],
#             'trade_wizard-current_step': '2',
#         },
#         {
#             'limited_tendering': ['Model Limited Tendering Reason'],
#             'trade_wizard-current_step': '3',
#         }
#     )
    
#     def test_initial_call(self):
#         response = self.client.get(reverse(self.wizard_urlname, args=['0']))
#         self.assertEqual(response.status_code, 200)
#         wizard = response.context['wizard']
#         self.assertEqual(wizard['steps'].current, '0')
#         self.assertEqual(wizard['steps'].step0, 0)
#         self.assertEqual(wizard['steps'].step1, 1)
#         self.assertEqual(wizard['steps'].last, '2')
#         self.assertEqual(wizard['steps'].prev, None)
#         self.assertEqual(wizard['steps'].next, '1')
#         self.assertEqual(wizard['steps'].count, 3)
#         self.assertEqual(wizard['url_name'], self.wizard_urlname)
# import unittest

# def fun(x):
#     return x + 1

# class MyTest(unittest.TestCase):
#     def test(self):
#         self.assertEqual(fun(3), 4)
