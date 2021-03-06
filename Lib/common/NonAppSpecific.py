"""
Methods that can be used for every site.
"""
import os
import sys
import time
import json
import pyautogui
from selenium import webdriver
from selenium.common.exceptions import MoveTargetOutOfBoundsException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from Lib.common.WaitAction import wait_until


def wait_page_load(driver):
    """
    Wait page to load
    """
    wait_until(lambda: driver.execute_script("return document.readyState;") == "complete", timeout=30)

def send_text(element, text, mode="set"):
    """
    Send text with mode set or update. Set mode types into input field. Update mode first clear
    text from input field and then types text.

    :param element: Element for input text
    :type element: WebElement
    :param text: Text to input
    :type text: str
    :param mode: Possible values are set and update. Update will clear existing text and put new text,
    mode set will add to existing text.
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
    """
    Return path to folder where images are
    :param folderName: Name of folder in folder Images (example: Tour1)
    :return: path
    """
    path = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, 'Images', os.path.basename(os.getcwd()),folderName))
    return path

def get_location(driver, element):
    """
    Get location of element inside of browser

    :param driver: Driver
    :param element: Element location (top right corner of element)
    :return:
    """
    # if "safari" in inspect.getfile(driver.__class__):
    #     location = driver.execute_script("return arguments[0].getBoundingClientRect()", element)
    # else:
    #     location = element.location
    before = driver.execute_script("return window.pageYOffset")
    driver.execute_script("scroll(0,0)")
    location = driver.execute_script("return arguments[0].getBoundingClientRect()", element)
    driver.execute_script("scroll(0,{})".format(before))
    return location

def getConfigurationPath():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       os.pardir, os.pardir, "Configuration"))

def change_config_username_pass_value(value, file='SgPano\\test.json'):
    with open(os.path.join(getConfigurationPath(), file), 'r+') as f:
        data = json.load(f)
        data['configuration']['payPalEmail'] = value  # <--- add `id` value.
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()


def check_if_elem_exist(func):
    """
    Execute function 'func' that returns element. Return true or false

    :param func: Function that return element
    :type func: func
    :return: If element is found return True, otherwise return False
    :rtype: bool
    """
    try:
        func()
        print("true")
        return True
    except Exception as ex:
        print("false")
        print(ex)
        return False

def click_on_element_intercepted(func):
    """
    Try to click on element. If another element is on top of this element (ElementClickInterceptedException)
    then method returns False.

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


def scroll_element_to_viewpoint_top(log, driver, element):
    """
    Scroll browser down or up so that element is at top of viewpoint.

    :param element: Element to show on top of viewpoint
    :type element: WebElement
    """
    log.info("Execute method scroll_to_element")
    driver.execute_script("scroll(0,{})".format(get_location(driver, element)["y"]))


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


def scroll_element_to_center(driver, log, element):
    """
    Scroll browser down or up so that element is on center of viewpoint.

    :param element: Element to scroll on center
    :type element: WebElement
    """
    size = element.size
    location = get_location(driver, element)
    viewPointHeight = driver.execute_script("return window.innerHeight")
    if viewPointHeight > size["height"]:
        pom = (viewPointHeight-size["height"])/2
        driver.execute_script("scroll(0,{})".format(location["y"] - pom))
    else:
        pom = (size["height"]-viewPointHeight)/2
        driver.execute_script("scroll(0,{})".format(location["y"] + pom))
    time.sleep(0.5)
    log.screenshot("Element scrolled to view")

# def scroll_element_to_viewPoint_with_selenium(driver, element):
#     """
#     Scroll browser down or up so that element is on center of viewpoint.
#
#     :param element: Element to scroll on center
#     :type element: WebElement
#     """
#     location = get_location(driver, element)
#     driver.execute_script("scroll(0,{})".format(location["y"]))


def is_location_on_viewpoint(driver, locationY):
    hiddenPixels = driver.execute_script("return window.pageYOffset")
    viewPointHeight = driver.execute_script("return window.innerHeight")
    if locationY < hiddenPixels + viewPointHeight and locationY > hiddenPixels:
        return True
    else:
        return False

def get_hidden_pixels(driver):
    """
    Return pixel size that is not currently on browser (hidden)
    """
    return driver.execute_script("return window.pageYOffset")

# def scroll_element_to_center_with_drag(driver, actionChains, fromElement, toElement):
#     """
#     Mouse on from element and its on view
#
#     :param element: Element to scroll on center
#     :type element: WebElement
#     """
#     fromSize = fromElement.size
#     fromLocation = get_location(driver, fromElement)
#
#     toSize = toElement.size
#     toLocation = get_location(driver, toElement)
#     viewPointHeight = int(driver.find_element_by_tag_name("html").get_attribute("clientHeight"))
#     moveBy = int(viewPointHeight / 2)
#     i = 1
#     if fromLocation["y"] < toLocation["y"]:
#         #down
#         onViewPoint = False
#         while not onViewPoint:
#             if not is_location_on_viewpoint(driver, get_location(driver, toElement)["y"]+int(toSize["height"]/2)):
#                 if i ==1:
#                     actionChains.move_by_offset(0, moveBy).perform()
#                 else:
#                     actionChains.move_by_offset(5, 0).perform()
#                 i +=1
#                 time.sleep(3)
#                 driver.execute_script("scrollBy(0,{})".format(moveBy))
#                 time.sleep(2)
#             else:
#                 actionChains.move_by_offset(5, 0).perform()
#                 onViewPoint = True
#     else:
#         #up
#         driver.execute_script("scroll(0,{})".format(toLocation["height"]))


# def scroll_element_to_center_with_drag(driver, actionChains, fromElement, toElement):
#     """
#     Mouse on from element and its on view
#
#     :param element: Element to scroll on center
#     :type element: WebElement
#     """
#     fromSize = fromElement.size
#     fromLocation = fromElement.location
#
#     toSize = toElement.size
#     toLocation = toElement.location
#     viewPointHeight = int(driver.find_element_by_tag_name("html").get_attribute("clientHeight"))
#     moveBy = int(viewPointHeight / 4)
#     print("vph {}".format(viewPointHeight))
#     if fromLocation["y"] < toLocation["y"]:
#         #na dole
#         print("na dole")
#         onViewPoint = False
#         while not onViewPoint:
#             if not is_location_on_viewpoint(driver, toElement.location["y"]+int(toSize["height"]/2)):
#                 print("before scroll")
#                 print("moveBy {}".format(moveBy))
#                 actionChains.move_by_offset(0, moveBy).perform()
#                 time.sleep(10)
#                 driver.execute_script("scrollBy(0,{})".format(moveBy))
#                 time.sleep(2)
#                 print("after scroll")
#             else:
#                 print("jeste na point")
#                 onViewPoint = True
#     else:
#         #na gore
#         print("na gore")
#         driver.execute_script("scroll(0,{})".format(toLocation["height"]))



    # viewPointHeight = int(driver.find_element_by_tag_name("html").get_attribute("clientHeight"))
    # if viewPointHeight > size["height"]:
    #     pom = (viewPointHeight-size["height"])/2
    #     driver.execute_script("scroll(0,{})".format(location["y"] - pom))
    # else:
    #     pom = (size["height"]-viewPointHeight)/2
    #     driver.execute_script("scroll(0,{})".format(location["y"] + pom))


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


def close_driver(driver):
    """
    Close driver and all handles

    :param driver: Driver
    :type driver: WebDriver
    """
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        driver.close()


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

def upload_scenes_windows(driver, driverName, log, imgs, scenes):
    from pywinauto.application import Application

    time.sleep(3)
    dialog_name = ""
    if driverName == "Firefox":
        dialog_name = "File Upload"
    elif driverName == "Chrome":
        dialog_name = "Open"
    app = Application().connect(title=dialog_name)
    app.Dialog.ComboBoxEx.Edit.type_keys(imgs)
    log.screenshot("Entered path to images", True)

    time.sleep(2)
    log.screenshot("Pre klika", True)
    app.dlg.Open.click()
    time.sleep(2)
    log.screenshot("Nakon klika",True)
    #ActionChains(driver).send_keys(Keys.ENTER).perform()
    app.Dialog.ComboBoxEx.Edit.type_keys(scenes)
    time.sleep(2)
    log.screenshot("Pre klika", True)
    app.dlg.Open.click()
    time.sleep(2)
    log.screenshot("Nakon klika", True)
    log.screenshot("Entered all images", True)