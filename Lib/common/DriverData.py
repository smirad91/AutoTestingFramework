"""
Class used for holding information about browser to test, device to test, orientation of device
"""
import json
import os
import platform
import time


import pyautogui
from selenium import webdriver
from selenium.webdriver import FirefoxProfile

from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import close_driver, is_forwarded


class DriverData:

    mobile = False
    mobileHeight = None
    mobileWidth = None
    driverName = ""
    fullHeight = None
    height = None
    width = None
    mobileToTest = None
    orientation = None
    tabHeight = None #for chrome

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
        if platform.system() in "Windows":
            from ctypes import windll
            if windll.user32.BlockInput(True) == 0:
               raise Exception("Not running script as admin")
        if is_forwarded("browser") is not None:
            driver = is_forwarded("browser")
        DriverData.driverName = driver
        if is_forwarded("mobile") is not None:
            mobileToTest = is_forwarded("mobile")
        if mobileToTest is not None:
            DriverData.mobile = True
        if is_forwarded("orientation") is not None:
            orientation = is_forwarded("orientation")
        DriverData.mobileToTest = mobileToTest
        DriverData.orientation = orientation
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
        elif driverString == "Safari":
            driver = self.create_safari_driver(mobileToTest, orientation)
        else:
            raise Exception("Supported drivers are Firefox and Chrome. You forwarded {}".format(driverString))
        return driver

    def create_firefox_driver(self, mobileToTest, orientation):
        """
        Create firefox driver

        :param mobileToTest: Mobile to test from file Configuration/MobileTesting.json (example: galaxyS9/S9+)
        :type mobileToTest: str
        :param orientation: Can be Landscape or Portrait
        :type orientation: str
        :return: WebDriver
        """
        if mobileToTest is not None:
            size = get_mobile_size(mobileToTest, orientation)
            driver = webdriver.Firefox()
            driver.set_window_size(size['width'], size['height'])
            innerWidth = driver.execute_script("return window.innerWidth")
            innerHeight = driver.execute_script("return window.innerHeight")
            browserWidth = size['width'] + (size['width'] - innerWidth)
            browserHeight = size['height'] + (size['height'] - innerHeight)
            driver.close()
            driver = webdriver.Firefox()
            driver.set_window_size(browserWidth, browserHeight)
        else:
            driver = webdriver.Firefox()
            driver.maximize_window()
           # self.get_set_browser_tab_section_height(driver)
        set_height_width(driver)
        return driver


    def create_chrome_driver(self, mobileToTest, orientation):
        """
        Create Chrome driver

        :param mobileToTest: Mobile to test from file Configuration/MobileTesting.json (example: galaxyS9/S9+)
        :type mobileToTest: str
        :param orientation: Can be Landscape or Portrait
        :type orientation: str
        :return: WebDriver
        """
        if mobileToTest is not None:
            driver = self.create_chrome_driver_mobile(mobileToTest, orientation)
        else:
            driver = self.create_chrome_driver_desktop()
        return driver

    def create_safari_driver(self, mobileToTest, orientation):
        """
        Create safari driver

        :param mobileToTest: Mobile to test from file Configuration/MobileTesting.json (example: galaxyS9/S9+)
        :type mobileToTest: str
        :param orientation: Can be Landscape or Portrait
        :type orientation: str
        :return: WebDriver
        """
        driver = webdriver.Safari()
        if mobileToTest is not None:
            size = get_mobile_size(mobileToTest, orientation)
            DriverData.mobileHeight = size["height"]
            DriverData.mobileWidth = size["width"]
            driver.set_window_size(size["width"], size["height"])
        else:
            driver.maximize_window()
        return driver

    def close(self):
        """
        Close driver and all handles (all tabs...)
        """
        close_driver(self.driver)

    def set_browser_tab_section_height_mobile(self):
        """
        Set DriverData.tabHeight, height of opened browser
        """
        if self.mobile and self.driverName == "Chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--disable-infobars")
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.maximize_window()
            time.sleep(1)
            self.get_set_browser_tab_section_height(driver)
            driver.close()
        # elif self.mobile and self.driverName == "Firefox":
        #     driver = webdriver.Firefox()
        #     driver.maximize_window()
        #     time.sleep(1)
        #     DriverData.tabHeight = self.get_set_browser_tab_section_height(driver)
        #     driver.close()

    def get_set_browser_tab_section_height(self, driver):
        """
        Return and set DriverData.tabHeight of browser

        :param driver: Created driver
        :type driver: WebDriver
        :return tabHeight
        """
        tabHeight = driver.get_window_size()["height"] - int(
            driver.find_element_by_tag_name("html").get_attribute("clientHeight"))
        DriverData.tabHeight = tabHeight
        return tabHeight

    def create_chrome_driver_mobile(self, mobileToTest, orientation):
        """
        Create chrome driver for mobile

        :param mobileToTest:
        :param orientation:
        :return:
        """
        self.set_browser_tab_section_height_mobile()
        chrome_options = webdriver.ChromeOptions()
        mobileSize = get_mobile_size(mobileToTest, orientation)
        DriverData.mobileHeight = mobileSize["height"]
        DriverData.mobileWidth = mobileSize["width"]
        deviceMetrics = {"deviceMetrics": mobileSize}
        chrome_options.add_experimental_option("mobileEmulation", deviceMetrics)
        chrome_options.add_argument("--disable-infobars")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.maximize_window()
        set_height_width(driver)
        return driver

    def create_chrome_driver_desktop(self):
        """
        Create chrome in desktop mode

        :return: WebDriver
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.maximize_window()
        set_height_width(driver)
        self.get_set_browser_tab_section_height(driver)
        return driver

def set_height_width(driver):
    """
    Set viewpoint of browser

    :param driver: For which driver to set viewpoint
    :type driver: WebDriver
    """
    DriverData.height = driver.execute_script("return window.innerHeight")
    DriverData.width = driver.execute_script("return window.innerWidth")


def get_mobile_size(mobileToTest, orientation):
    """
    Return mobile size from file Configuration/MobileTesting.json with wanted orientation.

    :param mobileToTest:
    :param orientation:
    :return:
    """
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

def set_firefox_mobile_size(driver, widthSize, heightSize):
    """
    Depricated. For Firefox version 57.
    """
    if DriverData.driverName == "Firefox":
        time.sleep(0.5)
        pyautogui.FAILSAFE = False
        pyautogui.moveTo(0, 0)
        time.sleep(0.5)
        pyautogui.keyDown("ctrl")
        pyautogui.keyDown("shift")
        pyautogui.typewrite("m")
        pyautogui.keyUp("ctrl")
        pyautogui.keyUp("shift")
        time.sleep(2)
        for i in range(9):
            pyautogui.press("tab")
            time.sleep(2)
        pyautogui.typewrite(str(widthSize))
        time.sleep(1)
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.typewrite(str(heightSize))
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(3)
        height = int(driver.find_element_by_tag_name("body").get_attribute("clientHeight"))
        width = int(driver.find_element_by_tag_name("body").get_attribute("clientWidth"))
        if height != heightSize:
            raise Exception(
                "Height not successfully set. Height set: {}, but should be {}".format(height, heightSize))
        if width != widthSize:
            raise Exception("Width not successfully set. Width set: {}, but should be {}".format(width, widthSize))


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


def move_mouse_to_middle_of_browser(log, driver):
    """
    Move mouse (hardware, not with selenium) to the middle of browser viewpoint.
    """
    log.info("Execute method move_mouse_to_middle_of_browser")
    fullHeight = driver.get_window_size()["height"]
    if DriverData.driverName == "Firefox":
        if DriverData.mobile:
            mobileHeight = driver.execute_script("return window.innerHeight")
            tabs = fullHeight - DriverData.height
            _move_to(int(DriverData.width / 2), int((mobileHeight / 2) + tabs), 1)
        else:
            width = driver.execute_script("return window.innerWidth")
            height = driver.execute_script("return window.innerHeight")
            tabs = fullHeight - height
            _move_to(int(width / 2), int(height / 2) + int(tabs), 1)
    elif DriverData.driverName == "Chrome":
        if DriverData.mobile:
            mobileHeight = int(driver.find_element_by_tag_name("html").get_attribute("clientHeight"))
            mobileWidth = int(driver.find_element_by_tag_name("html").get_attribute("clientWidth"))
            tabs = fullHeight - DriverData.height
            _move_to(int(mobileWidth / 2), int((mobileHeight / 2) + tabs), 1)
        else:
            width = driver.execute_script("return window.innerWidth")
            height = driver.execute_script("return window.innerHeight")
            tabs = fullHeight - height
            _move_to(int(width / 2), int(height / 2) + int(tabs), 1)

def _move_to(x, y, duration):
    """
    Move cursor (hardware - using pyautogui).

    :param x: X location on desktop to move to
    :param y: Y location on desktop to move to
    :param duration:
    """
    currentPosition = pyautogui.position()
    if currentPosition[0] == x and currentPosition[1] == y:
        pyautogui.moveRel(1, 1, duration)
    else:
        pyautogui.moveTo(x, y, duration)