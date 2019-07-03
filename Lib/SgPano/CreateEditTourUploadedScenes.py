"""
Class for manipulating with page https://sgpano.com/uploaded-scenes/
"""

import time
from selenium.webdriver.support import expected_conditions

from Lib.SgPano.CreateEditTourConnectScenes import ConnectScenesTour
from Lib.SgPano.CreateEditTourUploadScenes import UploadScenesTour
from Lib.common.CommonAction import CommonAction
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import check_if_elem_exist, scroll_element_to_center
from Lib.common.WaitAction import wait_until


class UploadedScenesTour(CommonAction):

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def inpSceneTitle(self, index):
        return self.driver.find_elements_by_css_selector("input[id='scence-title']")[index]

    def btnNext(self):
        return self.driver.find_element_by_css_selector("input[value='Next >>']")

    def btnDeleteSceneOk(self):
        return self.driver.find_element_by_css_selector("button[class='ajs-button ajs-ok']")

    def insert_scenes_title(self, scenes):
        """
        Insert scene title and click on next button.

        :param scenes: For given list of scenes go through each and insert title
        :type scenes: list[Scene]
        """
        self.log.info("Execute method insert_scenes_title with parameter scenes={}".format(''.join(scenes.__repr__())))
        foundScenes = self.driver.find_elements_by_css_selector(
            "div[class*='scence-image ']")
        for picture in scenes:
            for scene in foundScenes:
                if scene.find_element_by_tag_name("p").text == picture.fileName:
                    #inputTitle = scene.find_element_by_id("scence-title")
                    inputTitle = scene.find_element_by_css_selector("input[id*='scence-title']")
                    inputTitle.send_keys(picture.title)
                    time.sleep(1)
                    break
        self.btnNext().click()
        wait_until(lambda: check_if_elem_exist(ConnectScenesTour(self.driver).btnHotSpot), timeout=30, period=2)
        self.log.screenshot("Button next executed")


    def delete_uploaded_scene(self, title):
        """
        Delete uploaded scenes with title.

        :param title: Title of scene to delete
        :type title: str
        """
        self.log.info("Execute method delete_uploaded_scene with parameter={}".format(title))
        numberOfScenesBeforeDelete = len(self.get_uploaded_scenes())
        uploadedScenes = self.driver.find_elements_by_css_selector("div[class^='scence-image col-lg-12']")
        foundScene = False
        for scene in uploadedScenes:
            current_title = scene.find_element_by_css_selector("input[id*='scence-title']").get_attribute("value")
            if current_title == title:
                self.log.info("Delete scene with title={}".format(title))
                scroll_element_to_center(self.driver, self.log, scene.find_element_by_css_selector("div[class='icon-delete']"))
                scene.find_element_by_css_selector("div[class='icon-delete']").click()
                wait_until(lambda: check_if_elem_exist(self.btnDeleteSceneOk), timeout=10)
                wait_until(expected_conditions.alert_is_present, timeout=10)
                self.btnDeleteSceneOk()
                self.btnDeleteSceneOk().click()
                try:
                    wait_until(lambda: not check_if_elem_exist(self.btnDeleteSceneOk), timeout=10)
                except Exception as ex:
                    self.btnDeleteSceneOk().click()
                wait_until(lambda: numberOfScenesBeforeDelete - 1 == len(self.get_uploaded_scenes()), 30)
                wait_until(lambda: check_if_elem_exist(UploadScenesTour(self.driver).btnUpload), timeout=30, period=2)
                self.log.screenshot("Scene {} deleted".format(title))
                foundScene = True
                break
        if not foundScene:
            raise Exception("Scene with title {} not found".format(title))

    def get_uploaded_scenes(self):
        """
        Get current uploaded scenes

        :return: title of all uploaded scenes
        """
        self.log.info("Execute method get_uploaded_scenes")
        titles = []
        scenes = self.driver.find_elements_by_css_selector('input[id*="scence-title"]')
        for scene in scenes:
            titles.append(scene.get_attribute('value'))
        self.log.info("Uploaded scenes are={}".format(titles))
        return titles

