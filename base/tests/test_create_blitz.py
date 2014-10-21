# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestCreateBlitz(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_create_blitz(self):
        driver = self.driver
        driver.get(self.base_url + "/login?standard")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("mr@example.com")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        driver.find_element_by_css_selector("img").click()
        driver.get(self.base_url + "/blitz-setup")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("Mind & Body")
        driver.find_element_by_id("id_url_slug").clear()
        driver.find_element_by_id("id_url_slug").send_keys("new")
        driver.find_element_by_xpath("//button[@type='button']").click()
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        driver.find_element_by_css_selector("span.text").click()
        driver.find_element_by_id("datepicker").click()
        driver.find_element_by_link_text("27").click()
        driver.find_element_by_id("id_charge").clear()
        driver.find_element_by_id("id_charge").send_keys("boo")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_id("id_charge").clear()
        driver.find_element_by_id("id_charge").send_keys("50")
        driver.find_element_by_id("datepicker").click()
        driver.find_element_by_link_text("27").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_link_text(u"Invite clients →").click()
        driver.find_element_by_xpath("//div[@id='header']/div/div/div/a[3]/span[2]").click()
        driver.find_element_by_link_text("Pages").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_link_text("http://127.0.0.1:8000/Mike/new").click()
        driver.back()
        driver.find_element_by_link_text("http://127.0.0.1:8000/Mike/new/signup").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.back()
        driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Invite free client')])[3]").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("Jimmy McGee")
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys("jimmy@example.com")
        driver.find_element_by_xpath("//button").click()
        driver.get(self.base_url + "/logout")
    
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
