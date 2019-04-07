import time

from Lib.common.Log import Log
from Lib.common.NonAppSpecific import check_if_elem_exist
from Lib.common.WaitAction import wait_until


class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnTemasekproperties(self):
        return self.driver.find_element_by_css_selector("a[href='https://temasekproperties.com/wp-admin/']")

    def btnDownloads(self):
        return self.driver.find_element_by_css_selector("a[href='edit.php?post_type=download']")

    def go_to_downloads(self):
        self.btnTemasekproperties().click()
        wait_until(lambda: self.driver.find_element_by_tag_name("h1").text == "Dashboard", 20)
        self.btnDownloads().click()

    def go_to_user_profile(self):
        startElem = self.driver.find_element_by_css_selector("nav[id='header-navigation']").find_element_by_id("menu-item-9049")
        startElem.find_element_by_tag_name("a").click()
        time.sleep(1)
        startElem.find_element_by_css_selector("li[class*='menu-item-9129']").click()

    def go_to_listings(self):
        startElem = self.driver.find_element_by_css_selector("nav[id='header-navigation']")
        startElem.find_element_by_css_selector("a[href='https://temasekproperties.com/listings/']").click()
