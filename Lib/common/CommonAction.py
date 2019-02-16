"""Code that is used in more than 2 other classes. For example menu bar... This class need to be inherited.
    Example shown in file CreateEditTourConnectScenes.py"""
import time
import pyautogui
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

from Lib.common.DriverData import DriverData
from Lib.common.NonAppSpecific import scroll_to_element, scroll_up_by, scroll_element_to_center


class CommonAction:
    def btnSignUp(self):
        return self.driver.find_element_by_id("menu-main-menu").find_element_by_tag_name("a[href*='membership-levels']")

    def btnLogIn(self):
        return self.driver.find_element_by_id("menu-main-menu").find_element_by_css_selector("a[href*='wp-login']")

    def btnOpenMenu(self):
        return self.driver.find_element_by_css_selector("span[class='c-hamburger c-hamburger--htx']")

    def btnDahsboard(self):
        return self.driver.find_element_by_id("menu-main-menu").find_element_by_id("menu-item-2430").find_element_by_tag_name("a")

    def btnLogInMobile(self):
        return self.driver.find_element_by_css_selector("ul[class='sh-nav-mobile']").find_element_by_css_selector("a[href*='wp-login']")

    def btnSignUpMobile(self):
        return self.driver.find_element_by_css_selector("ul[class='sh-nav-mobile']").find_element_by_css_selector(
            "a[href*='membership-levels']")

    def click_on_element(self, func):
        """
        Try to click on element. If another element is on top of this element (ElementClickInterceptedException)
        then scroll_to_element is executed and try to click again

        :param element: Element to click on
        :type element: WebElement
        """
        try:
            scroll_element_to_center(self.driver, self.log, func())
            func().click()
        except ElementClickInterceptedException as ex:
            time.sleep(1)
            #scroll because of sticky-header that is on top of site when we scroll down
            pyautogui.press(Keys.ARROW_UP)
            pyautogui.press(Keys.ARROW_UP)
            time.sleep(1)
            func().click()

    def move_mouse_to_middle_of_element(self, element):
        """
        Moving mouse to the middle of the element. If element is not on viewpoint, scroll will be done.

        :param element: Element to move cursor
        :type element: WebElement
        """
        fullBrowserSize = self.driver.get_window_size()
        fullbrowserVisina = fullBrowserSize["height"]
        unutrasnjiDeoVisina = int(self.driver.find_element_by_tag_name("html").get_attribute("clientHeight"))
        lokacijaElementa = element.location["y"]
        self.driver.execute_script("scroll(0,{})".format(
                fullbrowserVisina - unutrasnjiDeoVisina + lokacijaElementa))
        addSticky = False
        try:
            time.sleep(1)
            element2 = self.driver.find_element_by_css_selector("div[class*='sh-sticky-header-active']")
            addSticky = True
            time.sleep(1)
            scroll_up_by(self.driver, int(element2.size["height"]))
        except:
            pass
        time.sleep(1)
        el3 = self.driver.find_element_by_css_selector("img[class='sh-image-url']")
        pyautogui.moveTo(el3.location["x"], el3.location["y"])


def get_hotSpots(log, driver):
    """
    Get all hotSpots on current scene

    :return: HotSpot elements
    :rtype: WebElement
    """
    log.info("Execute method get_hotSpots")
    allHotSpots = driver.find_elements_by_css_selector("div[class^='pnlm-hotspot-base']")
    log.info("Number of hotSpots are={}".format(len(allHotSpots)))
    return allHotSpots


def move_mouse_to_element(driver, log, element):
    """
    Move mouse with pyautogui library to element

    :param driver:
    :param element:
    """
    scroll_element_to_center(driver, log, element)
    hiddenPixels = driver.execute_script("return window.pageYOffset")

    tabHeight = DriverData.tabHeight
    size = element.size
    y = element.location["y"] + size["height"]/2 - hiddenPixels + tabHeight
    x = element.location["x"] + size["width"]/2
    pyautogui.moveTo(x, y, duration=1)
    time.sleep(1)