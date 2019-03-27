from Lib.common.Log import Log


class Downloads:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnAddNew(self):
        return self.driver.find_element_by_css_selector(
                "a[href='https://temasekproperties.com/wp-admin/post-new.php?post_type=download']")

    def go_to_add_new(self):
        self.btnAddNew().click()