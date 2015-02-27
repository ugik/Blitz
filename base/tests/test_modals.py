# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestModals(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.set_window_size(1300, 1000)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_modals(self):
        driver = self.driver
        driver.get(self.base_url + "/login")
        driver.find_element_by_css_selector("button.btn-outline-trans").click()
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("mr@example.com")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        driver.find_element_by_xpath("//li[2]/div").click()
        time.sleep(3)
        driver.find_element_by_id("edit_program").click()
        time.sleep(1)
        driver.find_element_by_css_selector("button.close").click()
        time.sleep(1)
        driver.find_element_by_id("edit_macros").click()
        time.sleep(1)
        driver.find_element_by_css_selector("#modalMacros > div.modal-dialog-full > div.modal-content-full > div.modal-header > button.close").click()
        time.sleep(1)
        driver.find_element_by_xpath("//li[4]/div").click()
        time.sleep(3)
        driver.find_element_by_id("edit_macros").click()
        time.sleep(1)
        driver.find_element_by_css_selector("#modalClientMacros > div.modal-dialog-full > div.modal-content-full > div.modal-header > button.close").click()
        time.sleep(1)
        driver.find_element_by_id("edit_program").click()
        time.sleep(1)
        driver.find_element_by_css_selector("button.close").click()
        time.sleep(1)
        driver.find_element_by_link_text("Pages").click()
        time.sleep(1)
        driver.find_element_by_id("add_group").click()
        time.sleep(1)
        driver.find_element_by_css_selector("button.close").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(1)
        driver.find_element_by_id("invite_free").click()
        time.sleep(1)
        driver.find_element_by_css_selector("button.close").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(1)
        driver.find_element_by_id("invite_client").click()
        time.sleep(1)
        driver.find_element_by_css_selector("button.close").click()
    
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
