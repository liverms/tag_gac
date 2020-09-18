# from guide.models import Organization, CommodityType, Code, ValueThreshold, LimitedTenderingReason, GeneralException, CftaException, BooleanTradeAgreement, NumericTradeAgreement, Language
# from guide.logic import FORMS, TEMPLATES, AGREEMENTS, url_name, done_step_name, determine_final_coverage, organization_rule, value_threshold_rule, code_rule, exceptions_rule, build_context_dict, process_form
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.firefox.webdriver import WebDriver
# import time
# from selenium.webdriver.support.ui import Select
# import unittest


# def step_through_form(self, estimated_value=1000000000, organization=None, commodity_type='Goods', 
#                             general_exception=None, cfta_exception=None, lt_page=True, limited_tendering_reason=None):
#     self.selenium.get(self.live_server_url + '/tag/0/')

#     if estimated_value < 0:
#         raise ValueError('Estimated value cannot be less than zero')

#     # Mandatory elements page
#     try:
#         estimated_value_input = self.selenium.find_element_by_name("0-estimated_value")
#         org_input = Select(self.selenium.find_element_by_name("0-entities"))
#         type_input = Select(self.selenium.find_element_by_name("0-type"))
#         code_input = Select(self.selenium.find_element_by_name("0-code"))
#     except:
#         raise Exception('Cannot find elements in mandatory elements page')

#     estimated_value_input.send_keys(estimated_value)
    
#     if organization:
#         valid_orgs = Organization.objects.values_list('name')
#         if organization not in valid_orgs:
#             raise ValueError('Organization not in model')
#         org = organization
#     else:
#         org = Organization.objects.filter(tc=False).\
#                 filter(goods_rule=False).\
#                 filter(ccfta=True).filter(ccofta=True).\
#                 filter(chfta=True).filter(cpafta=True).\
#                 filter(cpfta=True).filter(ckfta=True).\
#                 filter(cufta=True).filter(wto_agp=True).\
#                 filter(ceta=True).filter(cptpp=True).\
#                 filter(cfta=True).values_list('name')[0]

#     org_input.select_by_visible_text(org)

#     type_input.select_by_visible_text(commodity_type)

#     value = Code.objects.filter(type=commodity_type).values_list('code')[1]
#     code_input.select_by_visible_text(value)
    
#     time.sleep(1)
#     self.selenium.find_element_by_xpath('//button[@value="Next"]').click()

#     def checklist(element):
#         time.sleep(1)
#         if element:
#             element=element[0]
#             try:
#                 check = self.selenium.find_element_by_xpath(".//div[@class='checkbox']/span/label[contains(., '" + element + "')]/input")
#                 check.click()
#             except:
#                 raise Exception('Cannot find ' + element)

#         self.selenium.find_element_by_xpath('//button[@value="Next"]').click()

#     checklist(general_exception)
#     checklist(cfta_exception)
    
#     if lt_page:
#         checklist(limited_tendering_reason)

#     output = self.selenium.find_element_by_id('output').text
#     return output    


# class SeleniumTests(StaticLiveServerTestCase):
#     port = 8000
#     fixtures = ["guide/fixtures/db.json"]

#     wizard_urlname = url_name

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = WebDriver()
#         cls.selenium.implicitly_wait(5)

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()
    
#     def test_all_apply(self):
#         output = step_through_form(self)
        
#         for ta in AGREEMENTS:
#             self.assertIn(ta.upper(), output)

#     def test_low_estimated_value(self):
#         output = step_through_form(self, estimated_value=1, lt_page=False)

#         for ta in AGREEMENTS:
#             self.assertNotIn(ta.upper(), output)
    
#     #Entity none apply
#     def test_org_none_apply(self):
#         org = Organization.objects.filter(tc=False).\
#             filter(goods_rule=False).\
#             filter(ccfta=False).filter(ccofta=False).\
#             filter(chfta=False).filter(cpafta=False).\
#             filter(cpfta=False).filter(ckfta=False).\
#             filter(cufta=False).filter(wto_agp=False).\
#             filter(ceta=False).filter(cptpp=False).\
#             filter(cfta=False).values_list('name')[0]

#         output = step_through_form(self, organization=org, lt_page=False)
#         for ta in AGREEMENTS:
#             self.assertNotIn(ta.upper(), output)

#     def test_goods_rule(self):
#         org = Organization.objects.filter(goods_rule=True).values_list('name')[0]

#         output = step_through_form(self, organization=org)

#         self.assertIn(AGREEMENTS[-1].upper(), output)
#         for ta in AGREEMENTS[:-1]:
#             self.assertNotIn(ta.upper(), output)

#     def test_tc_rule(self):
#         org = Organization.objects.filter(tc=True).values_list('name')[0]
        
#         output = step_through_form(self, organization=org, commodity_type='Construction')
        
#         self.assertIn(AGREEMENTS[-1].upper(), output)
#         for ta in AGREEMENTS[:-1]:
#             self.assertNotIn(ta.upper(), output)

#     def test_general_exception_cfta_applies(self):
#         ge = GeneralException.objects.\
#             filter(ccfta=True).filter(ccofta=True).\
#             filter(chfta=True).filter(cpafta=True).\
#             filter(cpfta=True).filter(ckfta=True).\
#             filter(cufta=True).filter(wto_agp=True).\
#             filter(ceta=True).filter(cptpp=True).\
#             filter(cfta=False).values_list('name')[0]
#         output = step_through_form(self, general_exception=ge)
  
#         self.assertIn(AGREEMENTS[-1].upper(), output)
#         for ta in AGREEMENTS[:-1]:
#             self.assertNotIn(ta.upper(), output)

#     def test_general_exception_none_applies(self):
#         ge = GeneralException.objects.\
#             filter(ccfta=True).filter(ccofta=True).\
#             filter(chfta=True).filter(cpafta=True).\
#             filter(cpfta=True).filter(ckfta=True).\
#             filter(cufta=True).filter(wto_agp=True).\
#             filter(ceta=True).filter(cptpp=True).\
#             filter(cfta=True).values_list('name')[0]
#         output = step_through_form(self, general_exception=ge, lt_page=False)

#         for ta in AGREEMENTS:
#             self.assertNotIn(ta.upper(), output)
