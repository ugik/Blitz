# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestDashboard(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.set_window_size(1200, 1000)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_dashboard(self):
        driver = self.driver
        driver.get(self.base_url + "/login?standard")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("mr@example.com")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Everything" in driver.page_source, "Text not found")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Hey boys" in driver.page_source, "Text not found")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        time.sleep(2)
        self.assertTrue("logged a workout" in driver.page_source, "Text not found")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("div.item-inner").click()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("missed a workout" in driver.page_source, "Text not found")
        driver.find_element_by_css_selector("button.btn.btn-default").click()
        driver.find_element_by_css_selector("button.btn.btn-default").click()
        driver.find_element_by_xpath("//li[2]/div").click()
        time.sleep(5)
#        import pdb; pdb.set_trace()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_link_text("Edit Program").click()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Tell a spotter how you" in driver.page_source, "Text not found")
        driver.find_element_by_css_selector("button.close").click()
        driver.find_element_by_link_text("Edit Macros").click()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Set macros for" in driver.page_source, "Text not found")
        driver.find_element_by_css_selector("#modalMacros > div.modal-dialog-full > div.modal-content-full > div.modal-header > button.close").click()
        driver.find_element_by_xpath("//li[5]/div").click()
        time.sleep(10)
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_link_text("Add").click()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("macros for" in driver.page_source, "Text not found")
        driver.find_element_by_css_selector("#modalClientMacros > div.modal-dialog-full > div.modal-content-full > div.modal-header > button.close").click()
        driver.find_element_by_xpath("//div[3]/ul/li[2]").click()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_xpath("//div[3]/ul/li[3]").click()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_xpath("//li[1]/div").click()
        time.sleep(5)
        driver.find_element_by_xpath("//li[4]/div").click()
        time.sleep(5)
        self.assertTrue("burrito" in driver.page_source, "Text not found")
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

