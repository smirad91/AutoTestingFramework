"""
Class used for holding information about browser to test, device to test, orientation of device
"""
import json
import os
import time
from ctypes import windll

import pyautogui
from selenium import webdriver
from selenium.webdriver import FirefoxProfile

from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import close_driver, is_forwarded


class DriverData:

    mobile = False
    driver = ""
    fullHeight = None

    def __init__(self, driver="Firefox", mobileToTest=None, orientation="Portrait"):
        """
        Creates driver and hold arguments for mobileToTest and orientation. If mobileToTest is not forwarded
        driver will test like on computer.
        Another way to forward this parameters are from command line with arguments --browser,
        --config, --mobile, --orientation. Example of command:

        python Test.py --browser=Firefox --config=Case1 --mobile="galaxyS9/S9+" --orientation=Landscape

        :param driver: Driver name
        :type driver: str
        :param mobileToTest: Key value from MobileTesting.json file from Configuration folder
        :type mobileToTest: str
        :param orientation: Used only if mobileToTest is forwarded. Possible values: Portrait and Landscape
        :type orientation: str
        """
        if windll.user32.BlockInput(True) == 0:
            print("Not running as admin")
        if is_forwarded("browser") is not None:
            driver = is_forwarded("browser")
        DriverData.driver = driver
        if is_forwarded("mobile") is not None:
            mobileToTest = is_forwarded("mobile")
        if mobileToTest is not None:
            DriverData.mobile = True
        if is_forwarded("orientation") is not None:
            orientation = is_forwarded("orientation")
        self.driver = self._create_driver(driver, mobileToTest, orientation)
        self.log = Log(self.driver)
        if mobileToTest is not None:
            self.log.info("Driver to create is={}, on mobile={} and orientation={}".format(driver, mobileToTest, orientation))
        else:
            self.log.info("Driver to create is={}. Testing on desktop computer".format(driver))


    def get_driver(self):
        """
        Get driver instance
        :return: Driver instance (WebDriver)
        """
        return self.driver

    def _create_driver(self, driverString, mobileToTest, orientation):
        """
        Create driver instance
        :param driverString: Browser name
        :type driverString: str
        user_pref("devtools.responsive.userAgent", "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/12.0 Mobile/15A372 Safari/604.1");

        :return: driver
        :rtype: WebDriver  devtools.responsive.userAgent
        """
        if driverString == "Firefox":
            driver = self.create_firefox_driver(mobileToTest, orientation)
        elif driverString == "Chrome":
            driver = self.create_chrome_driver(mobileToTest, orientation)
        else:
            raise Exception("Supported drivers are Firefox and Chrome. You forwarded {}".format(driverString))
        return driver

    def create_firefox_driver(self, mobileToTest, orientation):
        if mobileToTest is not None:
            fprofile = FirefoxProfile()
            size = self.get_mobile_size(mobileToTest, orientation)
            fprofile.set_preference("devtools.responsive.viewport.width", size["width"])
            fprofile.set_preference("devtools.responsive.viewport.height", size["height"])
            driver = webdriver.Firefox(firefox_profile=fprofile)
            driver.maximize_window()
            time.sleep(3)
            pyautogui.keyDown("ctrl")
            pyautogui.keyDown("shift")
            pyautogui.typewrite("m")
            pyautogui.keyUp("ctrl")
            pyautogui.keyUp("shift")
        else:
            driver = webdriver.Firefox()
            driver.maximize_window()
        return driver

    def create_chrome_driver(self, mobileToTest, orientation):
        if mobileToTest is not None:
            chrome_options = webdriver.ChromeOptions()
            mobileSize = self.get_mobile_size(mobileToTest, orientation)
            deviceMetrics = {"deviceMetrics": mobileSize}
            chrome_options.add_experimental_option("mobileEmulation", deviceMetrics)
            chrome_options.add_argument("--disable-infobars")
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.maximize_window()
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--disable-infobars")
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.maximize_window()
        return driver

    def get_mobile_size(self, mobileToTest, orientation):
        cl = ConfigLoader(file="MobileTesting.json", lookArgs=False)
        size = cl.get(mobileToTest).split("*")
        firstSize = int(size[0])
        secondSize = int(size[1])
        if orientation == "Portrait":
            if firstSize > secondSize:
                x = secondSize
                y = firstSize
            else:
                x = firstSize
                y = secondSize
        elif orientation == "Landscape":
            if firstSize > secondSize:
                x = firstSize
                y = secondSize
            else:
                x = secondSize
                y = firstSize
        else:
            raise Exception("Allowed orientation is Portrait and Landscape. Forwarded orientation is {}".format(orientation))
        return {"width": x, "height": y}

    def close(self):
        close_driver(self.driver)


def get_standard_emulated_device_list(mobileToTest):
    """
    Return from preferences file from chrome mobile size
    """
    with open(os.getenv('LocalAppData') + "\\Google\\Chrome\\User Data\\Default\\Preferences",
              encoding="utf8", mode="r") as f:
        parsed = json.loads(f.read())
        allPhones = json.loads(parsed["devtools"]["preferences"]["standardEmulatedDeviceList"])
        for i in allPhones:
            if i["title"] == mobileToTest:
                deviceMetric = i["screen"]["horizontal"]
                break
    return deviceMetric
