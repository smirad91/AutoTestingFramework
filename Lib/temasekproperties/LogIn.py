from Lib.common.Log import Log
from Lib.common.NonAppSpecific import send_text


class LogIn:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnSignUp(self):
        return self.driver.find_element_by_css_selector("a[href='/registration-agent/']")

    def inpUsename(self):
        return self.driver.find_element_by_id("user_login")

    def inpPassword(self):
        return self.driver.find_element_by_id("user_pass")

    def btnLogIn(self):
        return self.driver.find_element_by_id("wp-submit")

    def go_to_sign_up(self):
        self.btnSignUp().click()

    def log_in(self, username, password):
        send_text(self.inpUsename(), username)
        send_text(self.inpPassword(), password)
        self.btnLogIn().click()
