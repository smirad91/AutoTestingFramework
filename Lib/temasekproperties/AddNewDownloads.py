import time

from Lib.common.WaitAction import wait_until
from selenium.webdriver.support.select import Select

from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import send_text, scroll_element_to_center, scroll_element_to_viewpoint_top, \
    upload_scenes_windows, check_if_elem_exist


class AddNewDownloads:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def inpName(self):
        return self.driver.find_element_by_css_selector("input[name='post_title']")

    def inpModelURL(self):
        return self.driver.find_element_by_id("mp_model_url")

    def divDownloadCategory(self):
        return self.driver.find_element_by_id("download_categorydiv")

    def divDownloadTags(self):
        return self.driver.find_element_by_id("tagsdiv-download_tag")

    def btnText(self):
        return self.driver.find_element_by_id("content-html")

    def txtDescription(self):
        return self.driver.find_element_by_css_selector("textarea[class='wp-editor-area']")

    def inpTag(self):
        return self.driver.find_element_by_id("new-tag-download_tag")

    def btnAddTag(self):
        return self.driver.find_element_by_class_name("tagadd")

    def inpEnableVariablePricing(self):
        return self.driver.find_element_by_id("edd_variable_pricing")

    def txtExcerpt(self):
        return self.driver.find_element_by_id("excerpt")

    def selAuthor(self):
        return self.driver.find_element_by_id("post_author_override")

    def inpSaveDraft(self):
        return self.driver.find_element_by_id("save-post")

    def aDownloadImage(self):
        return self.driver.find_element_by_css_selector("a[href*='media-upload']")

    def aUploadImage(self):
        return self.driver.find_element_by_xpath("//a[contains(text(),'{}')]".format("Upload Files"))

    def btnSelectFiles(self):
        return self.driver.find_element_by_id("__wp-uploader-id-1")

    def btnSetDownloadImage(self):
        return self.driver.find_element_by_css_selector("button[class='button media-button button-primary button-large media-button-select']")

    def change_to_text(self):
        self.btnText().click()

    def set_name(self, name):
        send_text(self.inpName(), name)

    def set_advertisement_status(self, status):
        advertisement = self.driver.find_element_by_xpath("//p[contains(text(), 'Advertisement Status')]/following-sibling::p")
        advertisement.find_element_by_css_selector("input[value='{}']".format(status)).click()

    def set_advertisement_type(self, type):
        advertisement = self.driver.find_element_by_xpath("//*[contains(text(), 'Advertisement Type')]/following-sibling::p")
        advertisement.find_element_by_css_selector("input[value='{}']".format(type)).click()

    def set_description(self, desc):
        send_text(self.txtDescription(), desc)
        #descriptionArea = self.driver.find_element_by_id("tinymce").find_element_by_tag_name("p")
        #self.driver.execute_script("arguments[0].textContent = arguments[1];", descriptionArea, desc)

    def set_model_url(self, url):
        send_text(self.inpModelURL(), url)

    def locate_download_category(self):
        scroll_element_to_viewpoint_top(self.log, self.driver, self.divDownloadCategory())
        self.log.screenshot()

    def locate_download_tags(self):
        scroll_element_to_viewpoint_top(self.log, self.driver, self.divDownloadTags())
        self.log.screenshot()

    def set_download_category(self, bedrooms, floorLevel, residential, tenor):
        """


        :param bedrooms: Serial number on bedrooms
        :param floorLevel:
        :param residential:
        :param tenor:
        :return:
        """
        bedroomsList = self.divDownloadCategory().find_element_by_id("download_category-58").\
            find_element_by_tag_name("ul").find_elements_by_tag_name('li')
        bedroomElement = bedroomsList[bedrooms-1].find_element_by_tag_name("input")
        self.driver.execute_script("arguments[0].click()", bedroomElement)
        #scroll_element_to_center(self.driver, self.log, bedroomElement)
        #bedroomElement.click()

        floorLevelList = self.divDownloadCategory().find_element_by_id("download_category-66").\
                    find_element_by_tag_name("ul").find_elements_by_tag_name('li')
        floorLevelElement = floorLevelList[floorLevel - 1].find_element_by_tag_name("input")
        self.driver.execute_script("arguments[0].click()", floorLevelElement)
        #scroll_element_to_center(self.driver, self.log, floorLevelElement)
        #floorLevelElement.click()

        residentialList = self.divDownloadCategory().find_element_by_id("download_category-72").\
                    find_element_by_tag_name("ul").find_elements_by_tag_name('li')
        residentialElement = residentialList[residential - 1].find_element_by_tag_name("input")
        self.driver.execute_script("arguments[0].click()", residentialElement)
        #scroll_element_to_center(self.driver, self.log, residentialElement)
        #residentialElement.click()

        tenorList = self.divDownloadCategory().find_element_by_id("download_category-77").\
                    find_element_by_tag_name("ul").find_elements_by_tag_name('li')
        tenorElement = tenorList[tenor - 1].find_element_by_tag_name("input")
        self.driver.execute_script("arguments[0].click()", tenorElement)

        #scroll_element_to_center(self.driver, self.log, tenorElement)
        #tenorElement.click()

    def add_tag(self, tag):
        expandButton = self.driver.find_element_by_id("tagsdiv-download_tag").find_element_by_tag_name("button")
        if "false" in expandButton.get_attribute("aria-expanded"):
            expandButton.click()
        send_text(self.inpTag(), tag)
        self.btnAddTag().click()

    def enable_variable_pricing(self):
        scroll_element_to_center(self.driver, self.log, self.inpEnableVariablePricing())
        self.inpEnableVariablePricing().click()
        self.log.screenshot()

    def set_excerpt(self, text):
        send_text(self.txtExcerpt(), text)
        self.log.screenshot()

    def choose_author(self, user):
        # self.selAuthor().click()
        # time.sleep(1)
        sel = Select(self.selAuthor())
        sel.select_by_visible_text(user)
        # self.selAuthor().find_element_by_xpath("/option[contains(text(),'{}')]".format(user)).click()
        time.sleep(1)
        self.log.screenshot()

    def save_draft(self):
        scroll_element_to_center(self.driver, self.log, self.inpSaveDraft())
        time.sleep(1)
        self.log.screenshot()
        #self.inpSaveDraft().click()
        self.driver.execute_script("arguments[0].click();", self.inpSaveDraft())

    def select_first_image(self):
        wait_until(lambda: len(self.driver.find_elements_by_css_selector("div[class='attachment-preview js--select-attachment type-image subtype-gif landscape']"))>0)
        self.driver.find_elements_by_css_selector("div[class='attachment-preview js--select-attachment type-image subtype-gif landscape']")[0].click()

    def set_download_image(self, upload=False):
        self.log.info("Execute method set_download_image")
        found = False
        firstTry = True
        while(not found):
            self.aDownloadImage().click()
            self.log.screenshot("kliknuto")
            #self.aUploadImage().click()
            #self.btnSelectFiles().click()
            #upload_scenes_windows(self.driver, DriverData.driverName, self.log, r"C:\Users\radlo\PycharmProjects\FromGitTemasek\Images\temasekproperties", "Webpr")
            if firstTry:
                self.select_first_image()
            time.sleep(2)
            self.log.screenshot("selektovan prvi")
            wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_css_selector("span[class='spinner']")), timeout=180)
            self.log.screenshot("Images are shown")
            self.btnSetDownloadImage().click()
            try:
                wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_css_selector("img[class='attachment-post-thumbnail size-post-thumbnail']")), timeout=600)
                print("Pronasao")
                found = True
            except Exception as ex:
                pass
            firstTry = False


