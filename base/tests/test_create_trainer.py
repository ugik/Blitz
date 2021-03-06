# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestCreateTrainer(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.set_window_size(1200, 1000)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_create_trainer(self):
        driver = self.driver
        driver.get(self.base_url + "/register-trainer")
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("Troy Polamalu")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("troy@example.com")
        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys("asdf")
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("asdf")
        Select(driver.find_element_by_id("timezone-select")).select_by_visible_text("US/Pacific")
        driver.find_element_by_xpath("//button").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | null | ]]
        driver.find_element_by_id("id_short_name").clear()
        driver.find_element_by_id("id_short_name").send_keys("Mike")
#        driver.find_element_by_xpath("//button").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_id("id_short_name").clear()
        driver.find_element_by_id("id_short_name").send_keys("troy")
        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys("asdf")
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("asdf")
        driver.find_element_by_id("id_price").clear()
        driver.find_element_by_id("id_price").send_keys("49.95")
#        driver.find_element_by_xpath("//button").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_xpath("//form/button").click()

        time.sleep(2)
        self.assertTrue("Logo" in driver.page_source, "Text not found")
        driver.get(self.base_url + "")
    
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
