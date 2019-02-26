"""
Class for manipulating with page https://sgpano.com/edit-scenes/
"""

import time

from Lib.common import DriverData
from Lib.common.Log import Log
from Lib.common.WaitAction import wait_until

class EditScenes:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnDeleteOk(self):
        return self.driver.find_element_by_css_selector("button[class='ajs-button ajs-ok']")

    def divScenes(self):
        return self.driver.find_elements_by_css_selector("div[class='col-lg-4 col-md-4 col-xs-12 col-sm-12']")

    def get_number_of_scenes(self):
        """
        Get number of scenes

        :return: Number of scenes
        :rtype: int
        """
        self.log.info("Execute method get_number_of_scenes")
        allScenesNumber = len(self.divScenes())
        self.log.info("All scenes number is={}".format(allScenesNumber))
        return allScenesNumber

    def find_scene_by_name(self, name):
        """
        Find scene by name. If there is multiple tours with same name, first tour will be returned.
        If tour not found exception will be raised.

        :param name: Tour name
        :type name: str
        :return: Tour
        :rtype: WebElement
        """
        self.log.info("Execute method find_scene_by_name with parameter name={}".format(name))
        sceneFound = False
        allScenes = self.divScenes()
        for scene in allScenes:
            if scene.find_element_by_tag_name("h3").text == name:
                sceneFound = True
                return scene
        if not sceneFound:
            raise Exception("Scene {} not found".format(name))

    def remove_tour_by_name(self, name):
        """
        Remove scene with name. If there is multiple tours with same name, first tour will be removed.

        :param name: Name of tour
        :type name: str
        """
        self.log.info("Execute method remove_tour_by_name with parameter name={}".format(name))
        scenesNumber = self.get_number_of_scenes()
        scene = self.find_scene_by_name(name)
        if scene:
            self.log.info("Click on delete button")
            scene.find_element_by_css_selector("a[class='scene_remove']").click()
            time.sleep(1)
            self.btnDeleteOk().click()
            wait_until(lambda: self.get_number_of_scenes() + 1 == scenesNumber, 10)
            self.log.screenshot("Scene is deleted")


    def view_tour_by_name(self, name):
        """
        Click on view for tour with name.

        :param name: Name of tour to view
        :type name: str
        """
        self.log.info("Execute method view_tour_by_name with parameter name={}".format(name))
        scene = self.find_scene_by_name(name)
        if DriverData.DriverData.mobile:
            link = scene.find_element_by_css_selector("a[title='View']").get_attribute("href")
            self.driver.get(link)
        else:
            tab_number_before = len(self.driver.window_handles)
            self.log.info("Number of tabs currently open={}".format(tab_number_before))
            if scene:
                scene.find_element_by_css_selector("a[title='View']").click()
            self.log.info("Check if view is opened in new tab")
            wait_until(lambda: len(self.driver.window_handles) == tab_number_before+1, 30)
            self.log.info("View is opened in new tab")
            self.driver.switch_to.window(self.driver.window_handles[1])
            wait_until(lambda: name in self.driver.title, timeout=30,
                       errorMessage="Wrong tour is opened= {}. Tour= {} should be opened".format(self.driver.title, name))

    def edit_tour(self, name):
        """
        Click on edit for tour with name=name.

        :param name: Name of tour to edit
        :type name: str
        """
        self.log.info("Execute method edit_tour with parameter name={}".format(name))
        scene = self.find_scene_by_name(name)
        if scene:
            #scene.find_element_by_css_selector("a[title='Edit']").click()
            scene.find_element_by_css_selector("a[title='Edit']").find_element_by_tag_name("i").click()
            time.sleep(2)
            self.log.info("Scene found and clicked on edit button")
