"""
Class used for holding information about browser to test, device to test, orientation of device
"""
import sys
from selenium import webdriver
from Lib.common.ConfigLoader import ConfigLoader
from Lib.common.NonAppSpecific import is_forwarded, close_driver
from Lib.common.Log import Log


class DriverData:

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
        forwardedDriver = is_forwarded("driver")
        if forwardedDriver is not None:
            driver = forwardedDriver
        self.driver = self._create_driver(driver)
        self.log = Log(self.driver)
        self.log.info("Driver to create is={}".format(driver))
        if is_forwarded("mobile") is not None:
            mobileToTest = is_forwarded("mobile")
        if mobileToTest is not None:
            self.log.info("Testing mobile={}".format(mobileToTest))
            if is_forwarded("orientation") is not None:
                orientation = is_forwarded("orientation")
            self.log.info("Orientation={}".format(orientation))
            mobileTesting = ConfigLoader("MobileTesting.json", False)
            mobileSize = mobileTesting.get(mobileToTest)
            size = mobileSize.split("*")
            if orientation == "Portrait":
                winSizeX = size[0]
                winSizeY = size[1]
            elif orientation == "Landscape":
                winSizeX = size[1]
                winSizeY = size[0]
            else:
                raise Exception("Orientation supported are Portrait and Landscape")
            self.driver.set_window_size(winSizeX, winSizeY)
            self.driver.set_window_position(0, 0)
        else:
            self.log.info("Testing on desktop computer")
            self.driver.maximize_window()


    def get_driver(self):
        """
        Get driver instance
        :return: Driver instance (WebDriver)
        """
        return self.driver

    def _create_driver(self, driverString):
        """
        Create driver instance
        :param driverString: Browser name
        :type driverString: str
        :return: driver
        :rtype: WebDriver
        """
        if driverString == "Firefox":
            driver = webdriver.Firefox()
        elif driverString == "Chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--disable-infobars")
            driver = webdriver.Chrome(chrome_options=chrome_options)
        else:
            raise Exception("Supported drivers are Firefox and Chrome")
        return driver

    def close(self):
        close_driver(self.driver)