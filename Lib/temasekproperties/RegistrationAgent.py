import time

from Lib.common.Log import Log
from Lib.common.NonAppSpecific import send_text


class RegistrationAgent:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def inpFirstName(self):
        return self.driver.find_element_by_css_selector("input[name='Fname_22']")

    def inpLastName(self):
        return self.driver.find_element_by_css_selector("input[name='Lname_23']")

    def inpCEA(self):
        return self.driver.find_element_by_css_selector("input[name='Textbox_24']")

    def inpMobileNumber(self):
        return self.driver.find_element_by_css_selector("input[name='Mobile_25']")

    def btnNext(self):
        return self.driver.find_element_by_css_selector("input[value='Next']")

    def sign_up(self, firstName, lastname, CEA, mobile):
        send_text(self.inpFirstName(), firstName)
        send_text(self.inpLastName(), lastname)
        send_text(self.inpCEA(), CEA)
        send_text(self.inpMobileNumber(), mobile)
        #self.btnNext().click()
        time.sleep(10)