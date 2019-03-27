"""
Class for manipulating with page https://sgpano.com/virtual-tour-singapore-dashboard/advertiser-detail-page/
"""

import time
from Lib.common.Log import Log

class EditProfile:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def inpContactName(self):
        return self.driver.find_element_by_id("contact_name")

    def inpContactDetail(self):
        return self.driver.find_element_by_id("contact_main")

    def inpEmail(self):
        return self.driver.find_element_by_id("contact_alt")

    def txtDescription(self):
        return self.driver.find_element_by_css_selector("textarea[name='description']")

    def btnSave(self):
        return self.driver.find_element_by_id("submit")

    def edit_profile(self, name, contactDetail, email, description):
        """
        Insert data for editing profile

        :param name:
        :param contactDetail:
        :param email:
        :param description:
        """
        self.log.info("Execute method edit_profile with parameters name={}, contactDetail={}, email={},"
                      " description={}".format(name, contactDetail, email, description))
        self.inpContactName().send_keys(name)
        self.inpContactDetail().send_keys(contactDetail)
        self.inpEmail().send_keys(email)
        self.txtDescription().send_keys(description)
        time.sleep(0.5)
        self.log.screenshot("Data is entered")
        self.btnSave().click()
        self.log.info("Button save is clicked")
        time.sleep(2)