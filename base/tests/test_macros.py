# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestMacros(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.set_window_size(1200, 1500)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_macros(self):
        driver = self.driver
        driver.get(self.base_url + "/login")
        driver.find_element_by_css_selector("button.btn-outline-trans").click()
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("mr@example.com")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        driver.find_element_by_xpath("//li[2]/div").click()
        driver.find_element_by_id("edit_macros").click()
        driver.find_element_by_xpath("(//button[@type='button'])[24]").click()
        driver.find_element_by_link_text("Beast Mode (+15%)").click()
        self.assertTrue("101" in driver.page_source, "Text not found")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_xpath("//div[5]/div/div/div/button").click()
        driver.find_element_by_xpath("//li[6]/div").click()
        driver.find_element_by_id("edit_macros").click()
        driver.find_element_by_xpath("//div[6]/div/div/div[2]/div/div/div/form/div/button").click()
        driver.find_element_by_xpath("//div[@id='modalClientMacros']/div/div/div[2]/div/div/div/form/div/div/ul/li[3]/a/span").click()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("101" in driver.page_source, "Text not found")

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
