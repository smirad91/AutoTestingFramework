import time

from Lib.common.Log import Log
from Lib.common.NonAppSpecific import send_text


class UserProfile:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def aEditInfo(self):
        return self.driver.find_element_by_css_selector("a[href='/user-profile/?a=edit']")

    def inpFirstName(self):
        return self.driver.find_element_by_id('first_name')

    def inpLastName(self):
        return self.driver.find_element_by_id('last_name')

    def inpEmail(self):
        return self.driver.find_element_by_id('user_email')

    def inpMobile(self):
        return self.driver.find_element_by_id('mobile_number')

    def btnSubmit(self):
        return self.driver.find_element_by_css_selector("button[name='submit']")

    def edit_info(self, firstName, lastName, email, mobile):
        self.aEditInfo().click()
        send_text(self.inpFirstName(), firstName, mode="update")
        send_text(self.inpLastName(), lastName, mode="update")
        send_text(self.inpEmail(), email, mode="update")
        send_text(self.inpMobile(), mobile, mode="update")
        self.log.screenshot()
        self.btnSubmit().click()
        time.sleep(3)

