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
        self.base_url = "http://127.0.0.1:8000"
        self.driver.set_window_size(1300, 1000)
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_basic(self):
        driver = self.driver
        # open | /login | 
        driver.get(self.base_url + "/login")
        # click | css=button.btn-outline-trans | 
        driver.find_element_by_css_selector("button.btn-outline-trans").click()
        # type | id=id_email | tay@example.com
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("tay@example.com")
        # type | id=id_password | asd
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asd")
        # click | css=button.obtn.obtn-comment | 
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        # assertTextPresent |  | The password you entered wasn't right.
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("The password you entered wasn't right." in driver.page_source, "Text not found")
        # type | id=id_password | asdf
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        # click | css=button.obtn.obtn-comment | 
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        # assertTextPresent |  | Did you hit your macros?
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Did you hit your macros?" in driver.page_source, "Text not found")

        # open | /client-checkin | 
        driver.get(self.base_url + "/client-checkin")
        # assertTextPresent |  | Time to update your
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Time to update your" in driver.page_source, "Text not found")
        # click | id=done_action | 
        driver.find_element_by_id("done_action").click()
        # open | /log-workout/1/M | 
        driver.get(self.base_url + "/log-workout/1/M")
        # assertTextPresent |  | Log what you lifted today
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("workout" in driver.page_source, "Text not found")
        # type | name=set-829-weight | 100

        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[4]/div/div/input").clear()
        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[4]/div/div/input").send_keys("90")
        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[4]/div[2]/div/input").clear
        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[4]/div[2]/div/input").send_keys("10")
        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[6]/div/div/input").clear()
        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[6]/div/div/input").send_keys("95")
        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[6]/div[2]/div/input").clear()
        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[6]/div[2]/div/input").send_keys("8")
        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[8]/div/div/input").clear()
        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[8]/div/div/input").send_keys("100")
        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[8]/div[2]/div/input").clear
        driver.find_element_by_xpath("//div[@id='collapse-deadlift']/div/div[8]/div[2]/div/input").send_keys("7")
        # open | / | 
        driver.get(self.base_url + "/")
        # assertTextPresent |  | Luke Walton
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Luke Walton" in driver.page_source, "Text not found")
        # open |  | /profile/c/8
        driver.get(self.base_url + "")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        # open | /profile/c/8/progress | 
        driver.get(self.base_url + "/profile/c/8/progress")
        # assertTextPresent |  | Lat Pulldown
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Deadlift" in driver.page_source, "Text not found")
        # open | /profile/c/8/checkins | 
        driver.get(self.base_url + "/profile/c/8/checkins")
        # assertTextPresent |  | hasn't completed any
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("hasn't completed any" in driver.page_source, "Text not found")
        # open | /logout | 
        driver.get(self.base_url + "/logout")
        # click | css=button.btn-outline-trans | 
        driver.find_element_by_css_selector("button.btn-outline-trans").click()
        # type | id=id_email | mr@example.com
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("mr@example.com")
        # type | id=id_password | asdf
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        # click | css=button.obtn.obtn-comment | 
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        # assertTextPresent |  | Everything
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Everything" in driver.page_source, "Text not found")
        # open | /salespage | 
        driver.get(self.base_url + "/salespage")
        # assertTextPresent |  | Below is a list of signup pages
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Below is a list of signup pages" in driver.page_source, "Text not found")
        # open | /blitz-setup?modalBlitz | 
        driver.get(self.base_url + "/blitz-setup?modalBlitz")
        # Warning: assertTextPresent may require manual changes
        # assertTextPresent |  | Create new Program
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        # type | id=id_title | Test
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("Test")
        # click | id=datepicker | 
        driver.find_element_by_id("datepicker").click()
        # click | xpath=(//button[@type='submit'])[4] | 

#        import pdb; pdb.set_trace()
        driver.find_element_by_id("create-group").click()
        time.sleep(2)
#        driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
        # Warning: assertTextPresent may require manual changes
        # assertTextPresent |  | This field is required.
        self.assertTrue("This field is required." in driver.page_source, "Text not found")

        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        # click | css=button.close | 
        driver.find_element_by_css_selector("button.close").click()
        # click | link=exact:http://127.0.0.1:8000/Mike/3weeks | 
        driver.find_element_by_link_text("http://127.0.0.1:8000/Mike/3weeks").click()
        # assertTextPresent |  | Personal Fitness Coaching with Mike Rashid
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Personal Fitness Coaching with Mike" in driver.page_source, "Text not found")
        # click | css=button.obtn.obtn-comment-half | 
        driver.find_element_by_css_selector("button.obtn.obtn-comment-half").click()
        # assertTextPresent |  | You're seconds away 
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("You're seconds away" in driver.page_source, "Text not found")
        # click | id=blitz-signup-submit | 
        driver.find_element_by_id("blitz-signup-submit").click()
        # assertTextPresent |  | This field is required.
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("This field is required" in driver.page_source, "Text not found")
        # open | /salespage | 
        driver.get(self.base_url + "/salespage")
        # click | link=exact:http://127.0.0.1:8000/Mike/3weeks/signup | 
        driver.find_element_by_link_text("http://127.0.0.1:8000/Mike/3weeks/signup").click()
        # assertTextPresent |  | You're seconds away
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("You're seconds away" in driver.page_source, "Text not found")
        # open | /sales-blitz?slug=3weeks&short_name=Mike&debug=True&key=WRT3MI | 
        driver.get(self.base_url + "/sales-blitz?slug=3weeks&short_name=Mike&debug=True&key=WRT3MI")
        # assertTextPresent |  | This is a preview of how your page will look
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("you deserve" in driver.page_source, "Text not found")
        # open | /client-setup/7?modalInvite&free | 
        driver.get(self.base_url + "/client-setup/7?modalInvite&free")
        # click | //form/button | 
        time.sleep(2)
#        driver.find_element_by_id("invite-client").click()
        # assertTextPresent |  | This field is required.
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
#        self.assertTrue("This field is required." in driver.page_source, "Text not found")
        # open | /client-setup/7?modalInvite | 
        driver.get(self.base_url + "/client-setup/7?modalInvite")
        # click | css=button.close | 
        time.sleep(3)
        driver.find_element_by_css_selector("button.close").click()
        # open | /program | 
        driver.get(self.base_url + "/program")
        # assertTextPresent |  | Programs
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Programs" in driver.page_source, "Text not found")
        # open | /upload | 
        driver.get(self.base_url + "/upload")
        # assertTextPresent |  | Training programs
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Training programs" in driver.page_source, "Text not found")
        # open | /dashboard | 
        driver.get(self.base_url + "/dashboard")
        # assertTextPresent |  | Everything
        self.assertTrue("Everything" in driver.page_source, "Text not found")
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        # open | /logout | 
        driver.get(self.base_url + "/logout")
        # click | css=button.btn-outline-trans | 
        driver.find_element_by_css_selector("button.btn-outline-trans").click()
        # type | id=id_email | spotter@example.com
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("spotter@example.com")
        # type | id=id_password | asdf
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("asdf")
        # click | css=button.obtn.obtn-comment | 
        driver.find_element_by_css_selector("button.obtn.obtn-comment").click()
        # assertTextPresent |  | These are Blitz spotter functions
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Home" in driver.page_source, "Text not found")
        # click | link=Trainers, Programs, and WorkoutPlans | 
        driver.find_element_by_link_text("Trainers, Programs And WorkoutPlans").click()
        # assertTextPresent |  | Here are the trainers and their Programs & WorkoutPlan status
        self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        self.assertTrue("Here are the trainers" in driver.page_source, "Text not found")
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
