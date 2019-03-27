"""
Class for manipulating with page https://sgpano.com/
"""
import time

from Lib.common.CommonAction import CommonAction
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import check_if_elem_exist, scroll_element_to_center
from Lib.common.WaitAction import wait_until


class HomePage(CommonAction):
    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def go_to_sign_up(self):
        """
        Click on sign up
        """
        self.log.info("Go to sign up page")
        if not self.btnSignUp().is_displayed():
            self.btnOpenMenu().click()
            self.btnSignUpMobile().click()
        else:
            self.btnSignUp().click()
        time.sleep(1)

    def go_to_log_in(self):
        """
        Click on log in
        """
        self.log.info("Go to log in page")
        if not self.btnLogIn().is_displayed():
            time.sleep(2)
            self.btnOpenMenu().click()
            wait_until(lambda: check_if_elem_exist(self.btnLogInMobile), timeout=20)
            scroll_element_to_center(self.driver, self.log, self.btnLogInMobile())
            self.btnLogInMobile().click()
        else:
            self.btnLogIn().click()
        time.sleep(1)