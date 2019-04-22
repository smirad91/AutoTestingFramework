"""
Class for manipulating with page https://sgpano.com/virtual-tour-singapore-dashboard/
"""

import time

from Lib.SgPano.CreateEditTourBasicInformation import BasicInformationTour
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import check_if_elem_exist, scroll_element_to_center
from Lib.common.WaitAction import wait_until


class Dashboard:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnCreateNewTour(self):
        #return self.driver.find_element_by_css_selector("a[href*='create-new-virtual-tour']")
        return self.driver.find_element_by_css_selector("img[src*='create1']")

    def btnViewEditTour(self):
        #return self.driver.find_element_by_css_selector("a[href*='edit-scenes']")
        return self.driver.find_element_by_css_selector("img[src*='edittour1']")

    def btnEditProfile(self):
        return self.driver.find_element_by_css_selector("img[src*='editprofile1']")

    def create_new_tour(self):
        """
        Click on create new tour
        """
        self.log.info("Execute method create_new_tour")
        wait_until(lambda: check_if_elem_exist(self.btnCreateNewTour), timeout=30)
        scroll_element_to_center(self.driver, self.log, self.btnCreateNewTour())
        wait_until(lambda: check_if_elem_exist(self.btnCreateNewTour))
        time.sleep(5)
        self.btnCreateNewTour().click()
        self.log.info("Create new tour button clicked")
        wait_until(lambda: check_if_elem_exist(BasicInformationTour(self.driver).inpTitle),
                   timeout=30, errorMessage="Create new tour not opened")

    def view_edit_tour(self):
        """
        Click on view edit tour
        """
        self.log.info("Go to view/edit tour")
        wait_until(lambda: check_if_elem_exist(self.btnViewEditTour), timeout=30)
        # self.driver.execute_script("arguments[0].scrollIntoView();", self.btnViewEditTour())
        # time.sleep(5)
        # self.btnViewEditTour().click()
        self.driver.execute_script("arguments[0].click();", self.btnViewEditTour())
        wait_until(lambda: not check_if_elem_exist(self.btnViewEditTour), timeout=30)

    def go_to_edit_profile(self):
        """
        Click on edit profile
        """
        self.log.info("Go to edit profile")
        self.btnEditProfile().click()
        time.sleep(2)