# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestPosts(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_posts(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("button.btn.btn-default").click()
        driver.find_element_by_name("message_content").clear()
        driver.find_element_by_name("message_content").send_keys("what's up Joe?")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        driver.find_element_by_xpath("//li[6]/div").click()
        driver.find_element_by_id("add-comment").click()
        driver.find_element_by_id("add-comment").clear()
        driver.find_element_by_id("add-comment").send_keys("D!")
        driver.find_element_by_id("add-comment-submit").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*D![\s\S]*$")
    
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
