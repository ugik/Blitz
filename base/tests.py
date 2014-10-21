from django.test import TestCase, Client
from django.http import HttpRequest
from base.views import *

class BlitzTestCase(TestCase):
    fixtures = ['base_testdata.json']

    def test_logins(self):
        resp = self.client.get('/login')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/login?standard')
        self.assertEqual(resp.status_code, 200)

    def test_pages(self):
        self.client.login(username='mr@example.com', password='asdf')
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/inbox', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/salespage', follow=True)
        self.assertEqual(resp.status_code, 200)
        import pdb; pdb.set_trace()
        self.assertContains(resp, "payment/credit card page")
        resp = self.client.get('/program', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/dashboard', follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/sales-blitz?slug=3weeks&short_name=Mike', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/client-setup/7', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/blitz-setup', follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/upload', follow=True)
        self.assertEqual(resp.status_code, 200)






