"""
Class for manipulating with page https://sgpano.com/tour/ when viewing tour
"""

import time
from Lib.SgPano.CreateEditTourConnectScenes import ConnectScenesTour
from Lib.common.CommonAction import get_hotSpots
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import check_if_elem_exist
from Lib.common.WaitAction import wait_until


class ViewTour:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnShowAllScenes(self):
        return self.driver.find_element_by_css_selector("img[alt='gallef']")

    def paneGallery(self):
        return self.driver.find_element_by_css_selector("div[id='gallerypane']")

    def tourImage(self):
        return self.driver.find_element_by_class_name("pnlm-dragfix")

    def get_current_scene_title(self):
        """
        Return current scene title
        :return: Scene title
        :rtype: str
        """
        self.log.info("Execute method get_current_scene_title")
        sceneTitle = self.driver.find_element_by_css_selector("div[id='titleDiv']").text
        self.log.info("Current scene title is={}".format(sceneTitle))
        return sceneTitle

    def open_scene(self, name):
        """
        Change current scene to scene with name=name

        :param name: Name of scene to open
        :type name: str
        """
        ConnectScenesTour(self.driver).wait_scene_load()
        self.tourImage().click()
        self.log.info("Execute method open_scene with parameter={}".format(name))
        time.sleep(2)
        if not self.driver.find_element_by_css_selector("div[id='gallerypane']").is_displayed():
            self.log.info("Click on button show all scenes")
            self.btnShowAllScenes().click()
            wait_until(lambda: self.paneGallery().is_displayed, timeout=30)
            self.log.screenshot("Gallery is displayed")
        self.driver.find_element_by_xpath("//h5[contains(text(),'{}')]".format(name)).click()
        ConnectScenesTour(self.driver).wait_scene_load()
        self.btnShowAllScenes().click()

    def _check_hotSpot_in_center(self, moveUp=False):
        """
        Check if hotSpot is in center of view. And it shows to scene title=goingToScene. If hotSpot is not found
        or hotSpot is not in center exception is raised.

        :param goingToScene: Scene title that hotSpot should point
        :type goingToScene: str
        """
        self.log.info("Execute method _check_hotSpot_in_center")
        for hotSpot in get_hotSpots(self.log, self.driver):
            try:
                hotSpotLocation = hotSpot.get_attribute("style")
                translate = hotSpotLocation.split("translate(")[1].split("px")[0]
                hotSpotLocationWidth = int(translate.split(".")[0])
                size = hotSpot.size
                centerOfBrowser = self.driver.find_element_by_tag_name("body").size["width"]/2
                self.log.info("Check if hotspot with x location={} is on center={}".format(hotSpotLocationWidth, centerOfBrowser))
                if abs(abs(hotSpotLocationWidth + size["width"]/2) - centerOfBrowser) < 500:  #allowed error of 500 pixels
                    self.log.screenshot("Hotspot is in center")
                    # self.log.info("Check if going to scene is as wanted")
                    # print("************")
                    # print(hotSpot.get_attribute("style"))
                    # print(hotSpot.get_attribute("class"))
                    # print(hotSpot.find_element_by_tag_name("span").find_element_by_tag_name("div").text)
                    # print("************")
                    # if not check_if_elem_exist(lambda: hotSpot.find_element_by_xpath(
                    #         "//span[contains(text(),'{}')]".format(goingToScene))):
                    #     self.log.info("HotSpot is not showing to {}".format(goingToScene))
                    #     break
                    # self.log.info("GointTo scene is as wanted")
                    return True
            except Exception as ex:
                pass
        raise Exception("Hotspot not found")

    def _check_hotSpot_in_center2(self):
        """
        Check if hotSpot is in center of view. And it shows to scene title=goingToScene. If hotSpot is not found
        or hotSpot is not in center exception is raised.

        :param goingToScene: Scene title that hotSpot should point
        :type goingToScene: str
        """
        self.log.info("Execute method _check_hotSpot_in_center2")
        for hotSpot in get_hotSpots(self.log, self.driver):
            try:
                hotSpotLocation = hotSpot.get_attribute("style")
                translate = hotSpotLocation.split("translate(")[1].split("px")[0]
                hotSpotLocationWidth = int(translate.split(".")[0])
                size = hotSpot.size
                centerOfBrowser = self.driver.find_element_by_tag_name("body").size["width"]/2
                self.log.info("Check if hotspot with x location={} is on center={}".format(hotSpotLocationWidth, centerOfBrowser))
                if abs(abs(hotSpotLocationWidth + size["width"]/2) - centerOfBrowser) < 500:  #allowed error of 500 pixels
                    self.log.screenshot("Hotspot is in center")
                    # self.log.info("Check if going to scene is as wanted")
                    # print("************")
                    # print(hotSpot.get_attribute("style"))
                    # print(hotSpot.get_attribute("class"))
                    # print(hotSpot.find_element_by_tag_name("span").find_element_by_tag_name("div").text)
                    # print("************")
                    # if not check_if_elem_exist(lambda: hotSpot.find_element_by_xpath(
                    #         "//span[contains(text(),'{}')]".format(goingToScene))):
                    #     self.log.info("HotSpot is not showing to {}".format(goingToScene))
                    #     break
                    # self.log.info("GointTo scene is as wanted")
                    return True
            except Exception as ex:
                pass
        raise Exception("Hotspot not found")

    def check_arrows(self, scenes):
        """
        Check hotSpots for given scenes for location and scene that it shows to

        :param scenes: List of scene
        :type scenes: list[Scene]
        """
        self.log.info("Execute method check_arrows with parameter={}".format("".join(scenes.__repr__())))
        cst = ConnectScenesTour(self.driver)
        for scene in scenes:
            self.open_scene(scene.title)
            cst.zoom_out(5)
            #self.tourImage().click()
            for i, hotSpot in enumerate(scene.hotSpots):
                rotateInfo = cst.rotate_scene(hotSpot.location, scene.width, True, True)
                time.sleep(2)
                self._check_hotSpot_in_center()
                time.sleep(2)
                if i < len(scene.hotSpots)-1:
                    print(1)
                    #cst.rotate(not rotateInfo[0], rotateInfo[1] - 1, True)
                    if rotateInfo[1] > 1:
                        print(2)
                        cst.rotate(not rotateInfo[0], 1, True)
                        cst.rotate(not rotateInfo[0], rotateInfo[1]-1, False)
                    else:
                        print(3)
                        cst.rotate(not rotateInfo[0], 1, True)

    def check_arrows2(self, scenes):
        """
        Check hotSpots for given scenes for location and scene that it shows to

        :param scenes: List of scene
        :type scenes: list[Scene]
        """
        self.log.info("Execute method check_arrows with parameter={}".format("".join(scenes.__repr__())))
        cst = ConnectScenesTour(self.driver)
        for scene in scenes:
            self.open_scene(scene.title)
            #self.tourImage().click()
            for i in range(36):
                rotateInfo = cst.rotate(True, 1, True)
                time.sleep(2)
                try:
                    self._check_hotSpot_in_center()
                    self.log.screenshot("Found hotspot")
                except Exception as ex:
                    pass
