"""Code that is used in more than 2 other classes. For example menu bar... This class need to be inherited.
    Example shown in file CreateEditTourConnectScenes.py"""
import time
import pyautogui
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

from Lib.common.DriverData import DriverData
from Lib.common.NonAppSpecific import scroll_up_by, scroll_element_to_center, \
    get_location, send_text, check_if_elem_exist, click_on_element_intercepted
from Lib.common.WaitAction import wait_until


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

    def inpPayPalEmail(self):
        return self.driver.find_element_by_css_selector("input[id='email']")

    def inpPayPalPass(self):
        return self.driver.find_element_by_css_selector("input[id='password']")

    def btnLogInPayPal(self):
        return self.driver.find_element_by_css_selector("button[id='btnLogin']")

    def btnContinuePayPal(self):
        return self.driver.find_element_by_css_selector("button[track-submit='choose_FI_interstitial']")

    def btnPayNow(self):
        return self.driver.find_element_by_css_selector("input[value='Pay Now']")

    def wait_paypal_opened(self, timeout):
        self.log.info("Execute method wait_paypal_opened()")
        wait_until(lambda: "PayPal" in self.driver.title, timeout=timeout)

    def pay_pal(self, payPalEmail, payPalPassword, timeout):
        self.wait_paypal_opened(timeout)
        self.log.info("Add PayPal credentials")
        wait_until(lambda: check_if_elem_exist(self.inpPayPalEmail), timeout=timeout)
        send_text(self.inpPayPalEmail(), payPalEmail, mode="update")
        send_text(self.inpPayPalPass(), payPalPassword, mode="update")
        self.log.screenshot("Credentials for PayPal are entered")
        self.btnLogInPayPal().click()
        wait_until(lambda: check_if_elem_exist(self.btnContinuePayPal), timeout=timeout)
        self.log.screenshot("Click on continue")
        time.sleep(5)
        wait_until(lambda: click_on_element_intercepted(self.btnContinuePayPal), timeout=timeout)
        wait_until(lambda: check_if_elem_exist(self.btnPayNow), timeout=timeout)
        self.log.screenshot("Click on pay now")
        #self.btnPayNow().click()
        time.sleep(1000)
        self.log.screenshot("Paid")

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
        lokacijaElementa = get_location(self.driver, element)["y"]
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
        pyautogui.moveTo(get_location(self.driver, el3)["x"], get_location(self.driver, el3)["y"])




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
    y = get_location(driver, element)["y"] + size["height"]/2 - hiddenPixels + tabHeight
    x = get_location(driver, element)["x"] + size["width"]/2
    pyautogui.moveTo(x, y, duration=1)
    time.sleep(1)

