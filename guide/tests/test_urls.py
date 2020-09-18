from django.test import TestCase
from django.urls import resolve, reverse


class UrlsTest(TestCase):
    '''
    Test redirects
    '''
    def test_redirect_one(self):
        resp = self.client.get('/')
        self.assertRedirects(resp, '/tag/form/0/', status_code=302)

    def test_redirect_two(self):
        resp = self.client.get('/anytext')
        self.assertRedirects(resp, '/tag/form/0/', status_code=302)

    def test_redirect_three(self):
        resp = self.client.get('/tag')
        self.assertRedirects(resp, '/tag/form/0/', status_code=302)

    def test_redirect_four(self):
        resp = self.client.get('/tag/anytext')
        self.assertRedirects(resp, '/tag/form/0/', status_code=302)

    def test_form_redirect_one(self):
        resp = self.client.get('/tag/form')
        self.assertRedirects(resp, '/tag/form/0/', status_code=302)

    def test_form_redirect_two(self):
        resp = self.client.get('/tag/form/anytext')
        self.assertRedirects(resp, '/tag/form/0/', status_code=302)

    def test_form_redirect_three(self):
        resp = self.client.get('/tag/form')
        self.assertRedirects(resp, '/tag/form/0/', status_code=302)

    def test_form_redirect_four(self):
        resp = self.client.get('/tag/form/anytext')
        self.assertRedirects(resp, '/tag/form/0/', status_code=302)
    
    
    '''
    Test forms show up or redirects occur
    '''
    def test_mandatory_elements(self):
        resp = self.client.get('/tag/form/0/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'mandatory_elements.html')

        url = reverse('guide:form_step', args=[0])
        self.assertEqual(url, '/tag/form/0/')
        resolver = resolve('/tag/form/0/')
        self.assertEqual(resolver.view_name, 'guide:form_step')

    def test_general_exceptions(self):
        resp = self.client.get('/tag/form/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'exceptions.html')

        url = reverse('guide:form_step', args=[1])
        self.assertEqual(url, '/tag/form/1/')
        resolver = resolve('/tag/form/1/')
        self.assertEqual(resolver.view_name, 'guide:form_step')
    
    def test_cfta_exceptions(self):
        resp = self.client.get('/tag/form/2/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cfta_exceptions.html')

        url = reverse('guide:form_step', args=[2])
        self.assertEqual(url, '/tag/form/2/')
        resolver = resolve('/tag/form/2/')
        self.assertEqual(resolver.view_name, 'guide:form_step')

    # def test_limited_tendering_redirect(self):
    #     resp = self.client.get('/tag/form/3/')
    #     self.assertRedirects(resp, '/tag/form/3/', status_code=302)

    def test_done_step(self):
        url = reverse('guide:done_step')
        self.assertEqual(url, '/tag/form/done/')

    def test_done_step_redirect(self):
        resp = self.client.get('/tag/form/done_step/')
        self.assertRedirects(resp, '/tag/form/0/', status_code=302)


    '''
    Test views and urls match
    '''
    def test_entities_autocomplete(self):
        url = reverse('guide:entities_autocomplete')
        self.assertEqual(url, '/tag/entities_autocomplete/')
        resolver = resolve('/tag/entities_autocomplete/')
        self.assertEqual(resolver.view_name, 'guide:entities_autocomplete')

    def test_type_autocomplete(self):
        url = reverse('guide:type_autocomplete')
        self.assertEqual(url, '/tag/type_autocomplete/')
        resolver = resolve('/tag/type_autocomplete/')
        self.assertEqual(resolver.view_name, 'guide:type_autocomplete')

    def test_code_autocomplete(self):
        url = reverse('guide:code_autocomplete')
        self.assertEqual(url, '/tag/code_autocomplete/')
        resolver = resolve('/tag/code_autocomplete/')
        self.assertEqual(resolver.view_name, 'guide:code_autocomplete')

    def test_open_pdf(self):
        url = reverse('guide:open_pdf')
        self.assertEqual(url, '/tag/open_pdf/')
        resolver = resolve('/tag/open_pdf/')
        self.assertEqual(resolver.view_name, 'guide:open_pdf')

    def test_form_start(self):
        url = reverse('guide:form_start')
        self.assertEqual(url, '/tag/form/')
        resolver = resolve('/tag/form/')
        self.assertEqual(resolver.view_name, 'guide:form_start')
