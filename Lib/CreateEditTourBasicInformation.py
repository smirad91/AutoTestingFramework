"""
Class for manipulating with page https://sgpano.com/create-new-virtual-tour/
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from Lib.common.NonAppSpecific import send_text
from Lib.common.Log import Log


class BasicInformationTour:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def inpTitle(self):
        return self.driver.find_element_by_id("title")

    def inpAddress(self):
        return self.driver.find_element_by_id("address")

    def inpWatermarkText(self):
        return self.driver.find_element_by_id("watermark")

    def txtDescription(self):
        return self.driver.find_element_by_id("formGroupExampleInput7")

    def rbtnPublicAccess(self, answer):
        radio_btns = self.driver.find_element_by_class_name("check-box_radio")
        return radio_btns.find_element_by_xpath("//span[contains(text(),'{}')]/preceding-sibling::input".format(answer))

    def btnSubmit(self):
        return self.driver.find_element_by_id("submit")

    def check_insert_basic_info_successfully(self):
        try:
            self.driver.find_element_by_xpath("//h3[contains(text(),'upload your scenes')]")
            return True
        except:
            return False

    def set_basic_info(self, title, address, description, watermark="", publicAccess=True, mode="set"):
        """
        Insert basic info for creating new tour

        :param title: Title of tour
        :type title: str
        :param address: Tour address
        :type address: str
        :param description: Tour description
        :type description: str
        :param watermark: Watermark
        :type watermark: str
        :param publicAccess: Choose radio button for public access
        :type publicAccess: bool
        :param mode: Possible values are set or update
        :type mode: str
        """
        self.log.info("Execute method set_basic_info with parameters title={}, address={}, description={},"
                      " watermark={}, publicAccess={}, mode={}".format(title, address, description, watermark,
                                                                       publicAccess, mode))
        if title:
            send_text(self.inpTitle(), title, mode=mode)
        if address:
            send_text(self.inpAddress(), address, mode=mode)
        if watermark:
            send_text(self.inpWatermarkText(), watermark, mode="update")
        if publicAccess:
            self.rbtnPublicAccess("Yes").click()
        else:
            self.rbtnPublicAccess("No").click()
        if description:
            send_text(self.txtDescription(), description, mode=mode)
        self.log.screenshot("Data entered. Click on button submit")
        self.btnSubmit().click()
        wait = WebDriverWait(self.driver, 30)
        wait.until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "div[class*='qq-upload-button']")))
        self.log.info("Submit done")





