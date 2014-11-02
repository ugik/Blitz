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
        self.driver.implicitly_wait(30)
        self.driver.set_window_size(800, 1000)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_basic(self):
        driver = self.driver
        driver.get(self.base_url + "/login")
        driver.find_element_by_css_selector("button.btn-outline-trans").click()
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("tay@example.com")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asd")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/client-checkin")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_id("done_action").click()
        driver.get(self.base_url + "/log-workout/1/M")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_name("set-829-weight").clear()
        driver.find_element_by_name("set-829-weight").send_keys("100")
        driver.find_element_by_name("set-829-reps").clear()
        driver.find_element_by_name("set-829-reps").send_keys("8")
        driver.find_element_by_name("set-830-weight").clear()
        driver.find_element_by_name("set-830-weight").send_keys("110")
        driver.find_element_by_name("set-830-reps").clear()
        driver.find_element_by_name("set-830-reps").send_keys("9")
        driver.find_element_by_name("set-831-weight").clear()
        driver.find_element_by_name("set-831-weight").send_keys("120")
        driver.find_element_by_name("set-831-reps").clear()
        driver.find_element_by_name("set-831-reps").send_keys("10")
        driver.get(self.base_url + "/")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/profile/c/8/progress")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/profile/c/8/checkins")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/logout")
        driver.find_element_by_css_selector("button.btn-outline-trans").click()
        # ERROR: Caught exception [unknown command [pause(1000)]]
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("mr@example.com")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/salespage")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/blitz-setup?modalBlitz")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("Test")
        driver.find_element_by_id("datepicker").click()
        driver.find_element_by_link_text("24").click()
        driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("button.close").click()
        driver.find_element_by_link_text("http://127.0.0.1:8000/Mike/3weeks").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_css_selector("button.obtn.obtn-comment-half").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_id("blitz-signup-submit").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/salespage")
        driver.find_element_by_link_text("http://127.0.0.1:8000/Mike/3weeks/signup").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/sales-blitz?slug=3weeks&short_name=Mike&debug=True&key=WRT3MI")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/client-setup/7?modalInvite&free")
        driver.find_element_by_xpath("//form/button").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/client-setup/7?modalInvite")
        driver.find_element_by_css_selector("button.close").click()
        driver.get(self.base_url + "/program")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/upload")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/dashboard")
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/logout")
        driver.find_element_by_css_selector("button.btn-outline-trans").click()
        # ERROR: Caught exception [unknown command [pause(1000)]]
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("spotter@example.com")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_link_text("Trainers, Programs, and WorkoutPlans").click()
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
