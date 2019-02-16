"""
Class for manipulating with page https://sgpano.com/membership-levels/
"""
import time

from Lib.common.Log import Log
from Lib.common.NonAppSpecific import check_if_elem_exist, send_text, click_on_element_intercepted
from Lib.common.WaitAction import wait_until


class SignUp:
    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnTrialPanotour(self):
        return self.driver.find_element_by_css_selector("a[href*='level=1']")

    def btnTrialPanotourMobile(self):
        return self.driver.find_element_by_class_name("pmpro_advanced_levels-compare_table_responsive").find_element_by_css_selector("a[href*='level=1']")

    def btnBasicPanotour(self):
        return self.driver.find_element_by_css_selector("a[href*='level=2']")

    def btnBasicPanotourMobile(self):
        return self.driver.find_element_by_class_name("pmpro_advanced_levels-compare_table_responsive").find_element_by_css_selector("a[href*='level=2']")

    def inpUsername(self):
        return self.driver.find_element_by_id("username")

    def inpPassword(self):
        return self.driver.find_element_by_id("password")

    def inpPasswordConfirm(self):
        return self.driver.find_element_by_id("password2")

    def inpMail(self):
        return self.driver.find_element_by_id("bemail")

    def inpMailConfirm(self):
        return self.driver.find_element_by_id("bconfirmemail")

    def cbxTermsAndConditions(self):
        return self.driver.find_element_by_id("tos")

    def btnSubmit(self):
        return self.driver.find_element_by_css_selector("input[value^='Submit and Confirm']")

    def btnPayPal(self):
        return self.driver.find_element_by_css_selector("input[value*='Check Out with PayPal']")

    def inpPayPalEmail(self):
        return self.driver.find_element_by_css_selector("input[id='email']")

    def inpPayPalPass(self):
        return self.driver.find_element_by_css_selector("input[id='password']")

    def btnLogInPayPal(self):
        return self.driver.find_element_by_css_selector("button[id='btnLogin']")

    def btnContinuePayPal(self):
        return self.driver.find_element_by_css_selector("button[track-submit='choose_FI_interstitial']")

    def btnPayNow(self):
        return self.driver.find_element_by_css_selector("input[value='Pay Now']")

    def is_opened_right_page(self, membership):
        """
        Check whether right page is opened

        :param membership: Trial, Basic...
        :type membership: str
        """
        wait_until(lambda: membership in self.driver.find_element_by_css_selector("div[class='pmpro_checkout-fields']").text, timeout=30,
                                                errorMessage="Not right page opened")
        self.log.info("Page for memebership {} is opened".format(membership))

    def wait_paypal_opened(self, timeout):
        self.log.info("Execute method wait_paypal_opened()")
        wait_until(lambda: "PayPal" in self.driver.title, timeout=timeout)

    def open_trial_panotour(self):
        """
        Click on button Select for membership Trial with 1 Panotour.
        """
        self.log.info("Execute method open_trial_panotour")
        if not self.btnTrialPanotour().is_displayed():
            self.btnTrialPanotourMobile().click()
        else:
            self.btnTrialPanotour().click()
        self.is_opened_right_page("Trial")

    def open_basic_panotour(self):
        """
        Click on button Select for membership Trial with 1 Panotour.
        """
        self.log.info("Execute method open_basic_panotour")
        wait_until(lambda: check_if_elem_exist(self.btnBasicPanotour), timeout=20)
        if not self.btnBasicPanotour().is_displayed():
            self.btnBasicPanotourMobile().click()
        else:
            self.btnBasicPanotour().click()
        self.is_opened_right_page("Basic")

    def _input_signup_info(self, username, password, mail):
        """
        Put sign up information on site

        :param username:
        :param password:
        :param mail:
        """
        self.inpUsername().send_keys(username)
        self.inpPassword().send_keys(password)
        self.inpPasswordConfirm().send_keys(password)
        self.inpMail().send_keys(mail)
        self.inpMailConfirm().send_keys(mail)
        self.cbxTermsAndConditions().click()
        self.log.screenshot("Sign up info is added")

    def sign_up_trial(self, username, password, mail, timeout=30):
        """
        Input credentials and sign up

        :param username: Username
        :param password: Password
        :param mail: Email
        :param timeout: Timeout to wait, after submit, for new page to open
        """
        self.log.info("Execute method _input_signup_info with parameters username={}, password={}, "
                      "mail={}, timeout={}".format(username, password, mail, timeout))
        self._input_signup_info(username, password, mail)
        self.log.info("Click on submit")
        self.btnSubmit().click()
        wait_until(lambda: self.driver.find_element_by_css_selector("div[class='titlebar-title sh-table-cell']/h2")
                   .text == "Membership Confirmation", timeout=timeout, period=2,
                   errorMessage="Problem with sign up. Check log screenshots")
        self.log.screenshot("Sign up is successful")

    def sign_up_paid(self, username, password, mail, payPalEmail, payPalPassword, timeout=40):
        """
        Sign up for accounts that are paid

        :param username: Username
        :param password: Password
        :param mail: Mail
        :param payPalEmail: PayPal email
        :param payPalPassword: PayPal password
        :param timeout: Timeout to wait for new page to show
        """
        self.log.info("Execute method sign_up_paid with parameters username={}, password={}, "
                      "mail={}, payPalEmail={}, payPalPassword={}, timeout={}".format(username, password,
                                                                                      mail, payPalEmail, payPalPassword,
                                                                                      timeout))
        self._input_signup_info(username, password, mail)
        self.btnPayPal().click()
        self.wait_paypal_opened(timeout)
        self.log.info("Add PayPal credentials")
        wait_until(lambda: check_if_elem_exist(self.inpPayPalEmail), timeout=timeout)
        send_text(self.inpPayPalEmail(), payPalEmail, mode="update")
        send_text(self.inpPayPalPass(), payPalPassword, mode="update")
        self.log.screenshot("Credentials for PayPal are entered")
        self.btnLogInPayPal().click()
        wait_until(lambda: check_if_elem_exist(self.btnContinuePayPal), timeout=timeout)
        self.log.screenshot("Click on continue")
        wait_until(lambda: click_on_element_intercepted(self.btnContinuePayPal), timeout=timeout)
        wait_until(lambda: check_if_elem_exist(self.btnPayNow), timeout=timeout)
        self.log.screenshot("Click on pay now")
        self.btnPayNow().click()
        time.sleep(15)
        self.log.screenshot("Paid")



