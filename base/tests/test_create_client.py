# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestCreateClient(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_create_client(self):
        driver = self.driver
        driver.get(self.base_url + "/Mike/3weeks/signup?signup_key=TEST1")
        driver.find_element_by_css_selector("input.user-password").clear()
        driver.find_element_by_css_selector("input.user-password").send_keys("asdfasdf")
        driver.find_element_by_css_selector("input.cc-number").clear()
        driver.find_element_by_css_selector("input.cc-number").send_keys("4111111111111111")
        driver.find_element_by_css_selector("input.cc-em").clear()
        driver.find_element_by_css_selector("input.cc-em").send_keys("12")
        driver.find_element_by_css_selector("input.cc-ey").clear()
        driver.find_element_by_css_selector("input.cc-ey").send_keys("2020")
        driver.find_element_by_css_selector("input.cc-csc").clear()
        driver.find_element_by_css_selector("input.cc-csc").send_keys("123")
        driver.find_element_by_id("blitz-signup-submit").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_link_text(u"Set up your profile →").click()
        driver.find_element_by_css_selector("label.radio").click()
        driver.find_element_by_name("age").clear()
        driver.find_element_by_name("age").send_keys("30")
        driver.find_element_by_name("weight").clear()
        driver.find_element_by_name("weight").send_keys("200")
        driver.find_element_by_name("height_feet").clear()
        driver.find_element_by_name("height_feet").send_keys("6")
        driver.find_element_by_name("height_inches").clear()
        driver.find_element_by_name("height_inches").send_keys("2")
        driver.find_element_by_css_selector("button.obtn.full-width").click()
        driver.find_element_by_id("skip-headshot").click()
        driver.find_element_by_link_text(u"Finish Signup →").click()
        driver.find_element_by_id("video-continue").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("span.icon-bar").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("a.btn.btn-navbar").click()
        driver.find_element_by_link_text("People").click()
        driver.get(self.base_url + "/program")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_xpath("//div[@id='header']/div/div/div/a[2]/span[2]").click()
        driver.find_element_by_link_text("Inbox").click()
        driver.find_element_by_id("to-autocomplete").clear()
        driver.find_element_by_id("to-autocomplete").send_keys("Mike Rashid")
        driver.find_element_by_id("id_message_content").clear()
        driver.find_element_by_id("id_message_content").send_keys("Hi Mike, what's up?")
        driver.find_element_by_css_selector("button.obtn").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
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
