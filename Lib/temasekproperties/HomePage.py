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
