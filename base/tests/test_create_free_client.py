# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestCreateFreeClient(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(800, 800)
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_create_free_client(self):
        driver = self.driver
        driver.get(self.base_url + "/client-signup?signup_key=TEST2")
        driver.find_element_by_name("password1").clear()
        driver.find_element_by_name("password1").send_keys("asdf")
        driver.find_element_by_name("password2").clear()
        driver.find_element_by_name("password2").send_keys("asdf")
        driver.find_element_by_xpath("//button").click()
        driver.find_element_by_id("video-continue").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("img.basic-tooltip.img-circle").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("img").click()
        driver.find_element_by_link_text("Go log it now").click()
        driver.find_element_by_name("set-829-weight").clear()
        driver.find_element_by_name("set-829-weight").send_keys("1")
        driver.find_element_by_name("set-829-weight").clear()
        driver.find_element_by_name("set-829-weight").send_keys("2")
        driver.find_element_by_name("set-829-weight").clear()
        driver.find_element_by_name("set-829-weight").send_keys("3")
        driver.find_element_by_name("set-829-weight").clear()
        driver.find_element_by_name("set-829-weight").send_keys("4")
        driver.find_element_by_name("set-829-weight").clear()
        driver.find_element_by_name("set-829-weight").send_keys("5")
        driver.find_element_by_name("set-829-weight").clear()
        driver.find_element_by_name("set-829-weight").send_keys("6")
        driver.find_element_by_name("set-830-weight").clear()
        driver.find_element_by_name("set-830-weight").send_keys("15")
        driver.find_element_by_name("set-831-weight").clear()
        driver.find_element_by_name("set-831-weight").send_keys("25")
        driver.find_element_by_css_selector("span.small").click()
        driver.find_element_by_link_text("Save These Sets").click()
        driver.find_element_by_css_selector("button.obtn.log-workout-submit").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_link_text("Like").click()
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
