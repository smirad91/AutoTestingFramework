"""
Methods that can be used for every site.
"""
import os
import time

import pyautogui
from selenium import webdriver
from selenium.common.exceptions import MoveTargetOutOfBoundsException, ElementClickInterceptedException
from selenium.webdriver import ActionChains


def send_text(element, text, mode="set"):
    """
    Send text with mode set or update. Set mode types into input field. Update mode first clear
    text from input field and then types text.

    :param element: Element for input text
    :type element: WebElement
    :param text: Text to input
    :type text: str
    :param mode: Possible values are set and update
    :type mode: str
    :return:
    """
    if mode is "set":
        element.send_keys(text)
    elif mode is "update":
        element.clear()
        element.send_keys(text)
    else:
        raise Exception("Possible values for mode are set and update. Given mode is={}".format(mode))


def get_images_path(folderName):
    path = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, 'Images', folderName))
    return path


def check_if_elem_exist(func):
    """
    Execute function 'element' that returns element.

    :param func: Function that return element
    :type func: func
    :return: If element is found return True, otherwise return False
    :rtype: bool
    """
    try:
        elem = func()
        return True
    except Exception as ex:
        return False

def click_on_element_intercepted(func):
    """
    Try to click on element. If another element is on top of this element (ElementClickInterceptedException)
    then scroll_to_element return False

    :param func: Element to click on
    :type func: func
    :return True if clicked, False if not clicked
    :rtype bool
    """
    try:
        func().click()
        return True
    except ElementClickInterceptedException as ex:
        return False


def scroll_to_element(log, driver, element):
    """
    Scroll browser down or up so that element is at top of viewpoint.

    :param element: Element to show on top of viewpoint
    :type element: WebElement
    """
    log.info("Execute method scroll_to_element")
    driver.execute_script("scroll(0,{})".format(element.location["y"]))


def scroll_down_by(log, driver, pixels):
    """
    Scroll browser down from current location for pixels number.

    :param pixels: Number of pixels to scroll
    :type pixels: int
    """
    log.info("Execute method scroll_down_by with parameter={}".format(pixels))
    driver.execute_script("scrollBy(0,{})".format(pixels))


def scroll_up_by(driver, pixels):
    """
    Scroll browser up from current location for pixels number.

    :param pixels: Number of pixels to scroll
    :type pixels: int
    """
    driver.execute_script("scrollBy(0,{})".format(pixels * -1))


def click_and_hold_with_scroll(log, driver, actionChains, func):
    """
    For element that is returned from func, execute click_and_hold, if not succeeded (MoveTargetOutOfBoundsException)
    first time then scroll to element and try again.

    :param actionChains: Action chains
    :type actionChains: ActionChains
    :param func: Function that return element
    :type func: function
    """
    try:
        actionChains.click_and_hold(func()).perform()
    except MoveTargetOutOfBoundsException as ex:
        scroll_to_element(log, driver, func())
        actionChains.click_and_hold(func()).perform()


def scroll_element_to_center(driver, element):
    """
    Scroll browser down or up so that element is on center of viewpoint.

    :param element: Element to scroll on center
    :type element: WebElement
    """
    size = element.size
    location = element.location
    viewPointHeight = int(driver.find_element_by_tag_name("html").get_attribute("clientHeight"))
    if viewPointHeight > size["height"]:
        pom = (viewPointHeight-size["height"])/2
        driver.execute_script("scroll(0,{})".format(location["y"] - pom))
    else:
        pom = (size["height"]-viewPointHeight)/2
        driver.execute_script("scroll(0,{})".format(location["y"] + pom))


def move_mouse_to_middle_of_browser(log, driver):
    """
    Move mouse to the middle of browser viewpoint.
    """
    log.info("Execute method move_mouse_to_middle_of_browser")
    height = int(driver.find_element_by_tag_name("html").get_attribute("clientHeight"))
    width = int(driver.find_element_by_tag_name("html").get_attribute("clientWidth"))
    pyautogui.moveTo(int(width/2), int(height/2), 1)

# def move_mouse_to_element(driver, element):
#     """
#     Move mouse with pyautogui library to element
#
#     :param driver:
#     :param element:
#     """
#     scroll_element_to_center(driver, element)
#     hiddenPixels = driver.execute_script("return window.pageYOffset")
#     size = element.size
#     y = element.location["y"] + size["height"]/2 - hiddenPixels + driver.get_window_size()["height"] -\
#         int(driver.find_element_by_tag_name("html").get_attribute("clientHeight"))
#     x = element.location["x"] + size["width"]/2
#     pyautogui.moveTo(x, y, duration=1)


def get_mobile_size_chrome(mobile):
    """
    Get mobile size by starting browser

    :param mobile: Mobile to get size for
    :return: (x,y)
    """
    chrome_options = webdriver.ChromeOptions()
    deviceMetrics = {"deviceName": mobile}
    chrome_options.add_experimental_option("mobileEmulation", deviceMetrics)
    chrome_options.add_argument("--disable-infobars")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://sgpano.com/")
    time.sleep(3)
    x = driver.execute_script("return window.innerWidth")
    y = driver.execute_script("return window.innerHeight")
    driver.close()
    return (x,y)


def close_driver(driver):
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        driver.close()