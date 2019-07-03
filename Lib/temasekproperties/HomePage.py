import time

from selenium.webdriver import ActionChains

from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import check_if_elem_exist, send_text, wait_page_load
from Lib.common.WaitAction import wait_until


class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnTemasekproperties(self):
        return self.driver.find_element_by_css_selector("a[href='https://temasekproperties.com/wp-admin/']")

    def btnDownloads(self):
        return self.driver.find_element_by_css_selector("a[href='edit.php?post_type=download']")

    def spnExpandMenu(self):
        return self.driver.find_element_by_css_selector("span[class='c-hamburger c-hamburger--htx']")

    def go_to_downloads(self):
        self.btnTemasekproperties().click()
        wait_until(lambda: self.driver.find_element_by_tag_name("h1").text == "Dashboard", 20)
        self.btnDownloads().click()

    def go_to_user_profile(self):
        if DriverData.mobile:
            self.spnExpandMenu().click()
            startElem = self.driver.find_element_by_css_selector("ul[class='sh-nav-mobile']").find_element_by_id("menu-item-9049")
        else:
            startElem = self.driver.find_element_by_css_selector("nav[id='header-navigation']").find_element_by_id("menu-item-9049")
        startElem.find_element_by_tag_name("a").click()
        time.sleep(1)
        startElem.find_element_by_css_selector("li[class*='menu-item-9129']").click()

    def go_to_listings(self):
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_css_selector("nav[id='header-navigation']")))
        if DriverData.mobile:
            self.spnExpandMenu().click()
            start_elem = self.driver.find_element_by_css_selector("nav[class='sh-header-mobile-dropdown']")
        else:
            start_elem = self.driver.find_element_by_id("header-navigation")
        start_elem.find_elements_by_css_selector("a[href='https://temasekproperties.com/listings/']")[0].click()

    def go_to_listings_nfe(self):
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_css_selector("nav[id='header-navigation']")))
        if DriverData.mobile:
            self.spnExpandMenu().click()
            start_elem = self.driver.find_element_by_css_selector("nav[class='sh-header-mobile-dropdown']")
        else:
            start_elem = self.driver.find_element_by_id("header-navigation")
        start_elem.find_elements_by_css_selector("a[href='https://temasekproperties.com/listings-nfe/']")[0].click()
#https://temasekproperties.com/listings-nfe/
    def go_to_resources_booked(self):
        if DriverData.mobile:
            self.spnExpandMenu().click()
            start_elem = self.driver.find_element_by_id("header-navigation-mobile")
        else:
            start_elem = self.driver.find_element_by_id("header-navigation") # for mobile: header-navigation-mobile
        start_elem.find_element_by_id("menu-item-9408").click()
        time.sleep(2)
        wait_until(lambda: "block" in self.driver.find_element_by_id("header-navigation").find_element_by_id("menu-item-9408").find_element_by_tag_name("ul").get_attribute("style"))
        self.driver.find_element_by_id("header-navigation").find_element_by_id("menu-item-9434").click()
        time.sleep(3)
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_id("DataTables_Table_0_processing")))
        wait_until(lambda: "none" in self.driver.find_element_by_id("DataTables_Table_0_processing").get_attribute("style"))
        self.log.screenshot("resource booked opened")

    def go_to_resources_booking(self):
        if DriverData.mobile:
            self.spnExpandMenu().click()
            start_elem = self.driver.find_element_by_css_selector("ul[class='sh-nav-mobile']")
        else:
            start_elem = self.driver.find_element_by_id("header-navigation") # for mobile: header-navigation-mobile
        start_elem.find_element_by_id("menu-item-9408").click()
        time.sleep(2)
        wait_until(lambda: "block" in start_elem.find_element_by_id("menu-item-9408").find_element_by_tag_name("ul").get_attribute("style"))
        start_elem.find_element_by_id("menu-item-9409").click()
        time.sleep(3)
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_css_selector("div[class='bookly-progress-tracker bookly-table']")))
        # wait_until(lambda: "none" in self.driver.find_element_by_id("DataTables_Table_0_processing").get_attribute("style"))
        self.log.screenshot("resource booking opened")
