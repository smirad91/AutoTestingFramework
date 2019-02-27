"""
Class for manipulating with page https://sgpano.com/wp-login.php
"""

import time
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import send_text, check_if_elem_exist
from Lib.common.WaitAction import wait_until


class LogIn:
    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def inpUsername(self):
        return self.driver.find_element_by_id("user_login")

    def inpPassword(self):
        return self.driver.find_element_by_id("user_pass")

    def btnLogIn(self):
        return self.driver.find_element_by_id("wp-submit")

    def cbxSocialID(self):
        return self.driver.find_element_by_class_name("heateor_ss_social_login_optin")

    def btnLoginWithFacebook(self):
        return self.driver.find_element_by_css_selector("i[title='Login with Facebook']")

    def inpFacebookEmail(self):
        return self.driver.find_element_by_css_selector("input[id='email']")

    def inpFacebookPass(self):
        return self.driver.find_element_by_css_selector("input[id='pass']")

    def btnLogInToFacebook(self):
        return self.driver.find_element_by_css_selector("button[id='loginbutton']")

    def log_in(self, username, password):
        """
        Insert log in parameters and click on log in

        :param username:
        :param password:
        """
        self.log.info("Execute method log_in with parameters: {}, {}".format(username, password))
        wait_until(lambda: check_if_elem_exist(self.inpUsername), timeout=20)
        wait_until(lambda: self.inpUsername().is_displayed, timeout=20)
        self.inpUsername().send_keys(username)
        self.inpPassword().send_keys(password)
        self.log.info("Click on log in button")
        self.btnLogIn().click()
        time.sleep(2)

    def log_in_social_media(self, email, password):
        """
        Log in with facebook account

        :param email: Email
        :param password: Password
        """
        self.log.info("Execute method log_in_social_media with parameters email={}, password={}".format(email, password))
        self.cbxSocialID().click()
        time.sleep(1)
        self.btnLoginWithFacebook().click()
        wait_until(lambda: len(self.driver.window_handles) == 2, timeout=10)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        wait_until(lambda: check_if_elem_exist(self.inpFacebookEmail), timeout=30)
        self.log.info("Facebook login page opened")
        send_text(self.inpFacebookEmail(), email, mode="update")
        send_text(self.inpFacebookPass(), password, mode="update")
        self.btnLogInToFacebook().click()
        time.sleep(10)
        self.log.screenshot("Should be logged on facebook")

