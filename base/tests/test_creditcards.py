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
        self.driver.set_window_size(1300, 1000)
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
        driver.find_element_by_css_selector("input.card-number").clear()
        driver.find_element_by_css_selector("input.card-number").send_keys("1231231234")
        driver.find_element_by_css_selector("input.card-expiry-month").clear()
        driver.find_element_by_css_selector("input.card-expiry-month").send_keys("12")
        driver.find_element_by_css_selector("input.card-expiry-year").clear()
        driver.find_element_by_css_selector("input.card-expiry-year").send_keys("2020")
        driver.find_element_by_css_selector("input.card-cvc").clear()
        driver.find_element_by_css_selector("input.card-cvc").send_keys("123")
        driver.find_element_by_id("blitz-signup-submit").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("input.card-number").clear()
        driver.find_element_by_css_selector("input.card-number").send_keys("4000000000000002")
        driver.find_element_by_id("blitz-signup-submit").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        time.sleep(1)

        driver.find_element_by_css_selector("input.card-number").clear()
        driver.find_element_by_css_selector("input.card-number").send_keys("4000000000000127")
        driver.find_element_by_css_selector("input.card-cvc").clear()
        driver.find_element_by_css_selector("input.card-cvc").send_keys("123")
        driver.find_element_by_id("blitz-signup-submit").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("input.card-number").clear()
        driver.find_element_by_css_selector("input.card-number").send_keys("4000000000000069")
        driver.find_element_by_css_selector("input.card-cvc").clear()
        driver.find_element_by_css_selector("input.card-cvc").send_keys("123")
        driver.find_element_by_id("blitz-signup-submit").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        time.sleep(1)
        driver.find_element_by_css_selector("input.card-number").clear()
        driver.find_element_by_css_selector("input.card-number").send_keys("4000000000000119")
        driver.find_element_by_css_selector("input.card-cvc").clear()
        driver.find_element_by_css_selector("input.card-cvc").send_keys("123")
        driver.find_element_by_id("blitz-signup-submit").click()
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
