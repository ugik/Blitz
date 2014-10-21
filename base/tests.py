from django.test import TestCase, Client
from django.http import HttpRequest
from base.views import *

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class SeleniumBlitz(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_selenium_blitz(self):
        driver = self.driver
        driver.get(self.base_url + "/login?standard")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("mr@example.com")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("boo")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        driver.find_element_by_css_selector("img.basic-tooltip.img-circle").click()
        driver.find_element_by_link_text("Progress").click()
        driver.find_element_by_link_text("History").click()
        driver.find_element_by_link_text("Check-ins").click()
        driver.find_element_by_css_selector("img").click()
        driver.find_element_by_link_text("Inbox").click()
        driver.find_element_by_link_text("Pages").click()
        driver.find_element_by_css_selector("button.obtn.obtn-comment-grn").click()
        driver.get(self.base_url + "")
        driver.find_element_by_link_text("Programs").click()
        driver.find_element_by_link_text("Dashboard").click()
        driver.find_element_by_css_selector("img").click()
        driver.find_element_by_css_selector("img").click()
        driver.find_element_by_css_selector("div.logout > a").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

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






