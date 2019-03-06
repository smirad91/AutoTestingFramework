"""
Class for manipulating with page https://sgpano.com/upload-scenes/
"""
import pyautogui
import time

import platform



from Lib.common.DriverData import DriverData
from Lib.common.CommonAction import CommonAction
from Lib.common.NonAppSpecific import get_images_path, check_if_elem_exist, scroll_element_to_center, wait_page_load
from Lib.common.Log import Log
from Lib.common.ScenesGetData import get_pictures_string
from Lib.common.WaitAction import wait_until


class UploadScenesTour(CommonAction):

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnUpload(self):
        return self.driver.find_element_by_css_selector("div[class='qq-upload-button-selector qq-upload-button']")

    def get_number_uploaded_scenes(self):
        """
        Get number of uploaded scenes

        :return: Number of uploaded scenes
        :rtype: int
        """
        self.log.info("Execute method get_number_uploaded_scenes")
        scenes = self.driver.find_elements_by_css_selector("div[class='scence-image col-lg-12 col-md-12 col-xs-12 col-sm-12']")
        numberOfScenes = len(scenes)
        self.log.info("Number of {} scenes".format(numberOfScenes))
        return numberOfScenes

    def upload_scenes(self, scenes, timeout=300):
        """
        Upload scenes and wait maximum of timeout for uploading.

        :param scenes: List of scenes
        :type scenes: list[Scene]
        :param timeout: Maximum time to wait for upload
        :type timeout: int
        """
        beforeUpload = self.get_number_uploaded_scenes()
        self.log.info("Execute method upload_scenes with parameters scenes={}, timeout={}".format(scenes, timeout))
        if platform.system() in "Windows":
            self.upload_scenes_windows(scenes)
        else:
            self.upload_scenes_mac(scenes)
        self.wait_scenes_uploaded(timeout)
        self.check_number_of_uploaded_scenes(beforeUpload, len(scenes))
        self.log.screenshot("Scenes are uploaded")

    def upload_scenes_mac(self, scenes):
        """
        Upload scenes for mac operating system. Forwarded scenes number and number of scenes
         path folder in Images folder must be the same.

        :param scenes: List of scenes
        :type scenes: list[Scene]
        """
        self.log.info("Execute method upload_scenes with parameters imagesPath={}".format(scenes))
        imgs = get_images_path(scenes[0].folder)
        self.log.info("Scenes path is: {}".format(imgs))
        wait_page_load(self.driver)
        self.btnUpload().click()
        wait_page_load(self.driver)
        #time.sleep(7)
        pyautogui.keyDown("win")
        pyautogui.keyDown("shift")
        pyautogui.typewrite("g")
        time.sleep(1)
        pyautogui.keyUp("win")
        pyautogui.keyUp("shift")
        self.log.screenshot("Button upload clicked", True)
        time.sleep(2)
        pyautogui.typewrite(imgs)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('right')
        time.sleep(1)
        pyautogui.keyDown("shift")
        time.sleep(1)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.keyUp("shift")
        time.sleep(2)
        self.log.screenshot("All scenes should be marked. Press enter.", True)
        pyautogui.press('enter')


    def upload_scenes_windows(self, scenes):
        """
        Upload scenes for windows operating system. Forwarded scenes number and number of scenes
         path folder in Images folder must be the same.

        :param scenes: List of scenes
        :type scenes: list[Scene]
        """
        from pywinauto.application import Application

        self.log.info("Execute method upload_scenes with parameters scenes={}".format(scenes))
        imgs = get_images_path(scenes[0].folder)
        self.log.info("Scenes path is: {}".format(imgs))
        scroll_element_to_center(self.driver, self.log, self.btnUpload())
        self.btnUpload().click()
        time.sleep(3)
        dialog_name = ""
        if DriverData.driverName == "Firefox":
            dialog_name = "File Upload"
        elif DriverData.driverName == "Chrome":
            dialog_name = "Open"
        app = Application().connect(title=dialog_name)
        app.Dialog.ComboBoxEx.Edit.type_keys(imgs)
        self.log.screenshot("Entered path to images", True)
        time.sleep(0.5)
        app.dlg.Open.click()
        app.Dialog.ComboBoxEx.Edit.type_keys(get_pictures_string(scenes))
        time.sleep(0.5)
        app.dlg.Open.click()
        self.log.screenshot("Entered all images", True)

    def wait_scenes_uploaded(self, timeout):
        """
        Wait for scenes to be uploaded.

        :param timeout: Maximum timeout to wait for uploading scenes
        :type timeout: int
        """
        self.log.info("Execute method wait_scenes_uploaded with parameters"
                      " timeout={}".format(timeout))
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_css_selector("h3[id='toplimit']")), timeout)

    def check_number_of_uploaded_scenes(self, numberBeforeUpload, numberToUpload):
        """
        Checks if number of uploaded scenes before uploading new scenes are increased by numberToUpload.
        Raise exception if scenes number=numberToUpload is not uploaded.

        :param numberBeforeUpload: Number of uploaded scenes before upload
        :type numberBeforeUpload: int
        :param numberToUpload: Uploaded scenes
        :type numberToUpload: int
        """
        self.log.info("Execute method check_number_of_uploaded_scenes with parameters "
                      "numberBeforeUpload={}, numberToUpload={}".format(numberBeforeUpload, numberToUpload))
        wait_until(lambda: numberBeforeUpload + numberToUpload == self.get_number_uploaded_scenes(), 30,
                   errorMessage="Number of files that should be loaded={} are not the "
                            "same as actual uploaded scenes".format(numberToUpload))
