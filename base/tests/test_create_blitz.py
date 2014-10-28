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
        self.driver.set_window_size(800, 1000)
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
        driver.find_element_by_css_selector("a.btn.btn-navbar").click()
        driver.find_element_by_link_text("Pages").click()
        driver.find_element_by_css_selector("button.obtn.obtn-comment-grn").click()
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("Mike's new thing")
        driver.find_element_by_id("datepicker").click()
        driver.find_element_by_link_text("26").click()
        driver.find_element_by_id("id_charge").clear()
        driver.find_element_by_id("id_charge").send_keys("49.99")
        driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_id("id_url_slug").clear()
        driver.find_element_by_id("id_url_slug").send_keys("new")
        driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
        driver.find_element_by_link_text(u"Invite clients →").click()
        driver.find_element_by_css_selector("a.btn.btn-navbar").click()
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
        driver.find_element_by_name("name").send_keys("Clyde Drexler")
        # ERROR: Caught exception [Error: Dom locators are not implemented yet!]
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("Clyde Drexler")
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys("clyde@example.com")
        # ERROR: Caught exception [Error: Dom locators are not implemented yet!]
        driver.find_element_by_link_text(u"Continue →").click()
        driver.find_element_by_xpath("//div[@id='header']/div/div/div/a[2]/span[3]").click()
        driver.find_element_by_link_text("Pages").click()
        driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Invite paid client')])[3]").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("Clyde Drexler")
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys("clyde@example.com")
        driver.find_element_by_name("price").clear()
        driver.find_element_by_name("price").send_keys("29.95")
        driver.find_element_by_xpath("//div[@id='modal']/div/div/div[2]/div/div/div/div[3]/form/button").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("Shawn Kemp")
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys("shawn@example.com")
        driver.find_element_by_name("price").clear()
        driver.find_element_by_name("price").send_keys("99.99")
        driver.find_element_by_name("invite").clear()
        driver.find_element_by_name("invite").send_keys("I've setup your program and we're ready to start")
        driver.find_element_by_xpath("//div[@id='modal']/div/div/div[2]/div/div/div/div[3]/form/button").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_link_text(u"Continue →").click()
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
