# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestBasic(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(800, 1000)
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_basic(self):
        driver = self.driver
        driver.get(self.base_url + "/login?standard")
        time.sleep(2)
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("mr@example.com")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("foo")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("img").click()
        time.sleep(2)
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("b.caret").click()
        driver.find_element_by_css_selector("ul.dropdown-menu > li > a").click()
        driver.find_element_by_css_selector("a.btn.btn-navbar").click()
        driver.find_element_by_link_text("Inbox").click()
        driver.find_element_by_css_selector("a.btn.btn-navbar").click()
        driver.find_element_by_link_text("Pages").click()
        time.sleep(2)
        driver.find_element_by_css_selector("button.obtn.obtn-comment-grn").click()
        driver.back()
        driver.find_element_by_link_text("http://127.0.0.1:8000/Mike/3weeks").click()
        driver.find_element_by_css_selector("button.obtn.obtn-comment-half").click()
        driver.back()
        driver.back()
        driver.find_element_by_link_text("http://127.0.0.1:8000/Mike/3weeks/signup").click()
        driver.back()
        time.sleep(2)
        driver.find_element_by_css_selector("button.obtn.full-width").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("button.obtn.obtn-comment-half").click()
        driver.find_element_by_id("why").clear()
        driver.find_element_by_id("why").send_keys("this is the why work with me section")
        driver.find_element_by_css_selector("form[name=\"SalesBlitz\"] > div.submit-container > button.obtn.obtn-comment-half").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.back()
        driver.back()
        driver.back()
        driver.back()
        driver.find_element_by_css_selector("a.btn.btn-navbar").click()
        driver.find_element_by_link_text("Programs").click()
        time.sleep(2)
        driver.find_element_by_css_selector("button.obtn.obtn-comment-grn").click()
        driver.back()
        driver.find_element_by_css_selector("a.btn.btn-navbar").click()
        driver.find_element_by_link_text("Dashboard").click()
        driver.find_element_by_css_selector("li.solo-client > div.item > img.img-circle.headshot").click()
        driver.find_element_by_xpath("//div[@id='dashboard']/div/ul/li[4]/div/img").click()
        driver.find_element_by_css_selector("img").click()
        driver.find_element_by_css_selector("img.basic-tooltip.img-circle").click()
        driver.find_element_by_link_text("Progress").click()
        driver.find_element_by_link_text("Check-ins").click()
        driver.find_element_by_link_text("History").click()
        driver.find_element_by_css_selector("img").click()
        time.sleep(2)
        driver.find_element_by_xpath("//img[@alt='Tayshawn Prince']").click()
        driver.find_element_by_css_selector("img").click()
        driver.find_element_by_css_selector("a.btn.btn-navbar").click()
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