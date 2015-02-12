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
        self.driver.implicitly_wait(30)
        self.driver.set_window_size(1300, 1000)
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
        driver.find_element_by_link_text(u"Set up your profile →").click()
        driver.find_element_by_css_selector("label.radio").click()
        driver.find_element_by_name("age").clear()
        driver.find_element_by_name("age").send_keys("30")
        driver.find_element_by_xpath("//form[@id='setupForm']/div[3]/label[2]").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.find_element_by_name("weight").clear()
        driver.find_element_by_name("weight").send_keys("100")
        driver.find_element_by_name("height_feet").clear()
        driver.find_element_by_name("height_feet").send_keys("1")
        driver.find_element_by_name("height_inches").clear()
        driver.find_element_by_name("height_inches").send_keys("80")
        driver.find_element_by_css_selector("button.obtn.full-width").click()
        driver.find_element_by_id("skip-headshot").click()
        driver.find_element_by_link_text(u"Finish Signup →").click()
        # Warning: assertTextPresent may require manual changes
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Log Workout").click()
#        import pdb; pdb.set_trace()
        driver.find_element_by_xpath("//div[2]/input").clear()
        driver.find_element_by_xpath("//div[2]/input").send_keys("90")
        driver.find_element_by_xpath("//div[3]/div[2]/input").clear()
        driver.find_element_by_xpath("//div[3]/div[2]/input").send_keys("95")
        driver.find_element_by_xpath("//div[3]/div[3]/input").clear()
        driver.find_element_by_xpath("//div[3]/div[3]/input").send_keys("7")
#        driver.find_element_by_xpath("//div[4]/div[2]/input").clear()
#        driver.find_element_by_xpath("//div[4]/div[2]/input").send_keys("100")
#        driver.find_element_by_xpath("//div[4]/div[3]/input").clear()
#        driver.find_element_by_xpath("//div[4]/div[3]/input").send_keys("8")

        driver.find_element_by_css_selector("span.small").click()
        time.sleep(1)
        driver.find_element_by_link_text("Save These Sets").click()
        driver.find_element_by_css_selector("button.obtn.log-workout-submit").click()
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
