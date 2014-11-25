# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestCreditCards(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.set_window_size(1200, 1000)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_creditcards(self):
        driver = self.driver
        driver.get(self.base_url + "/Mike/3weeks")
        driver.find_element_by_css_selector("button.obtn.obtn-comment-half").click()
        driver.find_element_by_css_selector("input.user-name").clear()
        driver.find_element_by_css_selector("input.user-name").send_keys("John Doe")
        driver.find_element_by_css_selector("input.user-email").clear()
        driver.find_element_by_css_selector("input.user-email").send_keys("john@example.com")
        driver.find_element_by_css_selector("input.user-password").clear()
        driver.find_element_by_css_selector("input.user-password").send_keys("asdfasdf")
        driver.find_element_by_css_selector("input.cc-number").clear()
        driver.find_element_by_css_selector("input.cc-number").send_keys("1231231234")
        driver.find_element_by_css_selector("input.cc-em").clear()
        driver.find_element_by_css_selector("input.cc-em").send_keys("12")
        driver.find_element_by_css_selector("input.cc-ey").clear()
        driver.find_element_by_css_selector("input.cc-ey").send_keys("2020")
        driver.find_element_by_css_selector("input.cc-csc").clear()
        driver.find_element_by_css_selector("input.cc-csc").send_keys("123")
        driver.find_element_by_id("blitz-signup-submit").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("input.cc-number").clear()
        driver.find_element_by_css_selector("input.cc-number").send_keys("4111111111111112")
        driver.find_element_by_id("blitz-signup-submit").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("input.cc-number").clear()
        driver.find_element_by_css_selector("input.cc-number").send_keys("4444444444444448")
        driver.find_element_by_css_selector("input.cc-csc").clear()
        driver.find_element_by_css_selector("input.cc-csc").send_keys("123")
        driver.find_element_by_id("blitz-signup-submit").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("input.cc-number").clear()
        driver.find_element_by_css_selector("input.cc-number").send_keys("4444444444444450")
        driver.find_element_by_css_selector("input.cc-csc").clear()
        driver.find_element_by_css_selector("input.cc-csc").send_keys("123")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("input.cc-number").clear()
        driver.find_element_by_css_selector("input.cc-number").send_keys("4222222222222220")
        driver.find_element_by_css_selector("input.cc-csc").clear()
        driver.find_element_by_css_selector("input.cc-csc").send_keys("123")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("input.cc-number").clear()
        driver.find_element_by_css_selector("input.cc-number").send_keys("5112000200000002")
        driver.find_element_by_css_selector("input.cc-csc").clear()
        driver.find_element_by_css_selector("input.cc-csc").send_keys("200")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("input.cc-number").clear()
        driver.find_element_by_css_selector("input.cc-number").send_keys("4457000300000007")
        driver.find_element_by_css_selector("input.cc-csc").clear()
        driver.find_element_by_css_selector("input.cc-csc").send_keys("901")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("input.cc-number").clear()
        driver.find_element_by_css_selector("input.cc-number").send_keys("341111111111111")
        driver.find_element_by_css_selector("input.cc-csc").clear()
        driver.find_element_by_css_selector("input.cc-csc").send_keys("1234")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
    
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
