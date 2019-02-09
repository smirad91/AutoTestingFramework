"""
Class used for holding information about browser to test, device to test, orientation of device
"""
import json
import os
import sys
from ctypes import windll
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from Lib.common.Log import Log
from Lib.common.NonAppSpecific import close_driver


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
        :return: driver
        :rtype: WebDriver
        """
        if driverString == "Firefox":
            fprofile = FirefoxProfile()
            fprofile.add_extension()
            fprofile.set_preference("general.useragent.override", "https://addons.mozilla.org/en-US/firefox/addon/uaswitcher/")#"Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36")
            capabilities = {'browserName': 'firefox',
                            'agent': {
                                    'deviceName': 'iPhone X'
                                }}
            #binary = FirefoxBinary("C:\Program Files\Mozilla Firefox/firefox")
            driver = webdriver.Firefox(firefox_profile=fprofile)#, firefox_binary=binary)
            driver.maximize_window()
        elif driverString == "Chrome":
            driver = self.create_chrome_driver(mobileToTest, orientation)
        else:
            raise Exception("Supported drivers are Firefox and Chrome. You forwarded {}".format(driverString))
        return driver

    def create_chrome_driver(self, mobileToTest, orientation):
        if mobileToTest is not None:
            chrome_options = webdriver.ChromeOptions()
            found_mobile = False
            if orientation == "Portrait":
                deviceMetrics = {"deviceName": mobileToTest}
            elif orientation == "Landscape":
                deviceMetric = None
                with open(os.getenv('LocalAppData') + "\\Google\\Chrome\\User Data\\Default\\Preferences",
                          encoding="utf8", mode="r") as f:
                    parsed = json.loads(f.read())
                    allPhones = json.loads(parsed["devtools"]["preferences"]["standardEmulatedDeviceList"])
                    for i in allPhones:
                        if i["title"] == mobileToTest:
                            deviceMetric = i["screen"]["horizontal"]
                            found_mobile = True
                            break
                deviceMetrics = {"deviceMetrics": deviceMetric}
            else:
                raise Exception("Orientation must be Portrait or Landscape, forwarded is {}".format(orientation))
            if orientation == "Landscape" and not found_mobile:
                raise Exception("Mobile {} not found for chrome driver".format(mobileToTest))
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

    def close(self):
        close_driver(self.driver)


def is_forwarded(argument):
    """
    Used for getting arguments from python command. Python command example:
    python Test.py --browser=Firefox --config=Case1 --mobile="galaxyS9/S9+" --orientation=Landscape

    :param argument: Argument name
    :type argument: str
    :return: Value of argument or None
    :rtype: None or str
    """
    try:
        for arg in sys.argv:
            if argument in arg.split("=")[0]:
                return arg.split("=")[1]
    except:
        pass


