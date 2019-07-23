"""
Class for manipulating with page https://sgpano.com/tour/ when viewing tour
"""

import time
from Lib.SgPano.CreateEditTourConnectScenes import ConnectScenesTour
from Lib.common.CommonAction import get_hotSpots
from Lib.common.DriverData import DriverData
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import check_if_elem_exist
from Lib.common.WaitAction import wait_until


class ViewTour:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnShowAllScenes(self):
        return self.driver.find_element_by_id("gallery")
        #return self.driver.find_element_by_css_selector("img[alt='gallef']")

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
        cst=ConnectScenesTour(self.driver)
        cst.wait_scene_load()
        self.log.info("Execute method open_scene with parameter={}".format(name))
        try:
            wait_until(lambda: not self.paneGallery().is_displayed, timeout=10)
        except Exception as ex:
            pass
        if not self.driver.find_element_by_css_selector("div[id='gallerypane']").is_displayed():
            self.log.info("Click on button show all scenes")
            #self.btnShowAllScenes().click()
            self.driver.execute_script("arguments[0].click();", self.btnShowAllScenes())
            time.sleep(2)
            wait_until(lambda: self.paneGallery().is_displayed, timeout=30)
            self.log.screenshot("Gallery is displayed")
        self.driver.find_element_by_xpath("//h5[contains(text(),'{}')]".format(name)).click()
        cst.wait_scene_load()
        cst.rotate(True, 1, True)
        cst.rotate(False, 1, True)
        #self.tourImage().click()
        self.btnShowAllScenes().click()

    def _check_hotSpot_in_center(self, goingToScene, view=False):
        """
        Check if hotSpot is in center of view. And it shows to scene title=goingToScene. If hotSpot is not found
        or hotSpot is not in center exception is raised.

        :param goingToScene: Scene title that hotSpot should point
        :type goingToScene: str
        """
        self.log.info("Execute method _check_hotSpot_in_center with gointTo scene parameter={}".format(goingToScene))
        for hotSpot in get_hotSpots(self.log, self.driver):
            try:
                hotSpotLocation = hotSpot.get_attribute("style")
                translate = hotSpotLocation.split("translate(")[1].split("px")[0]
                hotSpotLocationWidth = int(translate.split(".")[0])
                size = hotSpot.size
                centerOfBrowser = self.driver.find_element_by_tag_name("body").size["width"]/2
                self.log.info("Check if hotspot with x location={} is on center={}".format(hotSpotLocationWidth, centerOfBrowser))

                limit = self.tourImage().size["width"]

                if hotSpotLocationWidth>0 and hotSpotLocationWidth<centerOfBrowser*2 and abs(abs(hotSpotLocationWidth + size["width"]/2) - centerOfBrowser) < limit:  #allowed error of 500 pixels
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

    def _check_hotSpot_on_view(self):
        """
        Check if hotSpot is in center of view. And it shows to scene title=goingToScene. If hotSpot is not found
        or hotSpot is not in center exception is raised.

        :param goingToScene: Scene title that hotSpot should point
        :type goingToScene: str
        """
        self.log.info("Execute method _check_hotSpot_on_view")
        for hotSpot in get_hotSpots(self.log, self.driver):
            try:
                hotSpotLocation = hotSpot.get_attribute("style")
                translate = hotSpotLocation.split("translate(")[1].split("px")[0]
                hotSpotLocationWidth = int(translate.split(".")[0])
                size = hotSpot.size
                browserX = self.driver.find_element_by_tag_name("body").size["width"]
                self.log.info("Check if hotspot with x location={} is on view={}".format(hotSpotLocationWidth, browserX))
                #if browserX - (hotSpotLocationWidth + size["width"]) > 0:
                if hotSpotLocationWidth>=0 and hotSpotLocationWidth<self.tourImage().size["width"]:
                    self.log.screenshot("Hotspot is on view")
                    return True
            except Exception as ex:
                pass
        raise Exception("Hotspot not found")


    def check_arrows(self, scenes, view=False):
        """
        Check hotSpots for given scenes for location and scene that it shows to

        :param scenes: List of scene
        :type scenes: list[Scene]
        """
        self.log.info("Execute method check_arrows with parameter={}".format("".join(scenes.__repr__())))
        cst = ConnectScenesTour(self.driver)
        connect_scene = ConnectScenesTour(self.driver)
        for scene in scenes:
            time.sleep(1)
            self.open_scene(scene.title)
           # if not DriverData.mobile is True:
            for i in range(5):
                connect_scene.btnZoomOut().click()
            self.log.screenshot("****Nova scena otvorena")
            #self.tourImage().click()
            for i, hotSpot in enumerate(scene.hotSpots):
                number_rotate = cst.get_number_rotate(hotSpot.location, scene.width)
                print(type(number_rotate[0]))
                print(number_rotate[0])
                if number_rotate[0]:
                    where = "right"
                else:
                    where = "left"
                self.log.screenshot("***pocinje rotate prvi")
                cst.rotate2(["{}:{}".format(where, number_rotate[1])], False, view)
                self.log.screenshot("***zavrsen rotate prvi")
                time.sleep(2)
                if view:
                    self._check_hotSpot_on_view()
                else:
                    self._check_hotSpot_in_center(hotSpot.goingToScene, view)
                time.sleep(2)
                print(0)
                if not number_rotate[0]:
                    print(1)
                    where2 = "right"
                else:
                    print(2)
                    where2 = "left"
                if i < len(scene.hotSpots)-1:
                    self.log.screenshot("***pocinje rotate drugi")
                    rotate = []
                    if not view:
                        if hotSpot.up:
                            rotate.append("down:1")
                        if hotSpot.down:
                            rotate.append("up:3")
                    rotate.append("{}:{}".format(where2, number_rotate[1]))
                    cst.rotate2(rotate, False, view)
                    self.log.screenshot("***zavrsen rotate drugi")
                #     print(1)
                #     if rotateInfo[1] > 1:
                #         print(2)
                #         cst.rotate(not rotateInfo[0], 1, True)
                #         cst.rotate(not rotateInfo[0], rotateInfo[1]-1, False)
                #     else:
                #         print(3)
                #         cst.rotate(not rotateInfo[0], 1, True)
                self.log.screenshot("*****zavrsen prvi hotspot")

