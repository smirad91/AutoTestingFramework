import time

from selenium.webdriver import ActionChains

from Lib.common.Log import Log


class Downloads:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnNew(self):
        return self.driver.find_element_by_css_selector("a[href='https://temasekproperties.com/wp-admin/media-new.php']")

    def btnAddNew(self):
        return self.driver.find_element_by_css_selector(
                "a[href='https://temasekproperties.com/wp-admin/post-new.php?post_type=download']")

    def go_to_add_new(self):
        ActionChains(self.driver).move_to_element(self.btnNew()).perform()
        time.sleep(2)
        self.btnAddNew().click()
