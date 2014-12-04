# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestClientUsage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_client_usage(self):
        driver = self.driver
        # open | /login | 
        driver.get(self.base_url + "/login")
        # click | css=button.btn-outline-trans | 
        driver.find_element_by_css_selector("button.btn-outline-trans").click()
        # type | id=id_email | tay@example.com
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("tay@example.com")
        # type | id=id_password | asdf
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        # click | css=button.obtn.obtn-comment | 
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        driver.get(self.base_url + "/client-checkin")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")        #         # type | name=weight | 222
        driver.find_element_by_name("weight").clear()
        driver.find_element_by_name("weight").send_keys("222")
        # click | id=done_action | 
        driver.find_element_by_id("done_action").click()
        # assertTextPresent |  | Tayshaun Prince logged a check-in.
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        time.sleep(2)
        self.assertTrue("Tayshaun Prince</a> logged a" in driver.page_source, "Text not found")
        # Warning: assertTextPresent may require manual changes
        # assertTextPresent |  | 222
        self.assertTrue("222" in driver.page_source, "Text not found")        
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        # click | xpath=(//a[contains(text(),'Go log it now')])[4] | 
#        import pdb; pdb.set_trace()
        driver.find_element_by_xpath("(//a[contains(text(),'Go log it now')])[1]").click()
        time.sleep(3)
        # type | name=set-843-weight | 111
#        driver.find_element_by_name("set-843-weight").clear()
#        driver.find_element_by_name("set-843-weight").send_keys("111")
        # type | name=set-844-weight | 112
#        driver.find_element_by_name("set-844-weight").clear()
#        driver.find_element_by_name("set-844-weight").send_keys("112")
        # type | name=set-844-reps | 7
#        driver.find_element_by_name("set-844-reps").clear()
#        driver.find_element_by_name("set-844-reps").send_keys("7")
        # type | name=set-845-weight | 113
#        driver.find_element_by_name("set-845-weight").clear()
#        driver.find_element_by_name("set-845-weight").send_keys("113")
        # type | name=set-845-reps | 8
#        driver.find_element_by_name("set-845-reps").clear()
#        driver.find_element_by_name("set-845-reps").send_keys("8")
        # type | id=workout-notes | here's my workout
        driver.find_element_by_id("workout-notes").clear()
        driver.find_element_by_id("workout-notes").send_keys("here's my workout")
        # click | css=button.obtn.log-workout-submit | 
        driver.find_element_by_css_selector("button.obtn.log-workout-submit").click()
        # Warning: assertTextPresent may require manual changes
        # assertTextPresent |  | Tayshaun Prince logged a workout. 
        time.sleep(3)
        self.assertTrue("Tayshaun Prince</a> logged a workout." in driver.page_source, "Text not found")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        # click | id=add-comment | 
        driver.find_element_by_id("add-comment").click()
        # type | id=add-comment | Hey people!
        driver.find_element_by_id("add-comment").clear()
        driver.find_element_by_id("add-comment").send_keys("Hey people!")
        # click | id=add-comment-submit | 
        driver.find_element_by_id("add-comment-submit").click()
        # Warning: assertTextPresent may require manual changes
        # assertTextPresent |  | Hey people! 
        self.assertTrue("Hey people!" in driver.page_source, "Text not found")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        # open | /logout | 
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
