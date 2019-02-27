"""
Class for manipulating with page https://sgpano.com/connect-scenes/
"""

import pyautogui
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from Lib.common.CommonAction import CommonAction, get_hotSpots, move_mouse_to_element
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import scroll_element_to_center, check_if_elem_exist, send_text, \
    scroll_element_to_center_with_drag, scroll_element_to_viewPoint_with_selenium, get_location, get_hidden_pixels
from Lib.common.DriverData import move_mouse_to_middle_of_browser, DriverData
from Lib.common.WaitAction import wait_until


class ConnectScenesTour(CommonAction):

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def btnHotSpot(self):
        return self.driver.find_element_by_css_selector("img[src*='icon-room.png']")

    def btnInfo(self):
        return self.driver.find_element_by_css_selector("img[src*='icon-info.png']")

    def inpInfoTitle(self):
        return self.driver.find_element_by_css_selector("input[id='info_title']")

    def inpInfoDetail(self):
        return self.driver.find_element_by_css_selector("div[id='detailBox']")

    def inpInfoUrl(self):
        return self.driver.find_element_by_css_selector("input[id='info_url']")

    def btnInfoSave(self):
        return self.driver.find_element_by_css_selector("input[onclick='ajaxInfoHS()']")

    def btnDefaultView(self):
        return self.driver.find_element_by_css_selector("a[class='button-set-default']")

    def btnPanToView(self):
        return self.driver.find_element_by_css_selector("a[class='button-default-vew']")

    def btnViewTour(self):
        return self.driver.find_element_by_css_selector("a[class='button-hotspot']")

    def btnMoveRight(self):
        return self.driver.find_element_by_css_selector("img[src*='right-arrow']")

    def tourImage(self):
        return self.driver.find_element_by_class_name("pnlm-dragfix")

    def btnRighRotate(self):
        return self.driver.find_element_by_css_selector("img[src*='right-arrow.svg']")

    def btnLeftRotate(self):
        return self.driver.find_element_by_css_selector("img[src*='left-arrow.svg']")

    def btnDeleteHotSpot(self):
        wait_until(lambda: check_if_elem_exist(self.divHotSpotMenu), timeout=10)
        return self.divHotSpotMenu().find_element_by_css_selector("a[id*='hotSpotDelete']")

    def btnEditHotSpot(self):
        return self.divHotSpotMenu().find_element_by_css_selector("a[id*='hotSpotEdit']")

    def btnGoToHotSpot(self):
        return self.divHotSpotMenu().find_element_by_css_selector("a[id*='hotSpotGoto']")

    def btnSaveHotSpot(self):
        return self.driver.find_element_by_css_selector("div[style='text-align: center;']").find_element_by_id("submit")

    def btnSaveEditedHotSpot(self):
        return self.driver.find_element_by_css_selector("input[onclick='ajaxEditHotspot()']")

    def btnPublish(self):
        return self.driver.find_element_by_css_selector("input[value='Publish']")

    def btnChangeTheme(self):
        return self.driver.find_element_by_css_selector("a[class='button-changetheme']")

    def imgThemeToSelect(self, number):
        return self.driver.find_elements_by_css_selector("div[class*='thumbnail']")[number-1]

    def btnSelectTheme(self):
        return self.driver.find_element_by_css_selector("input[value='Choose Theme']")

    def divHotSpotMenu(self):
        allMenus = self.driver.find_elements_by_css_selector("div[class='hotSpotMenu']")
        for menu in allMenus:
            if "visible;" in menu.get_attribute("style"):
                return menu

    def btnSaveInfo(self):
        return self.driver.find_element_by_css_selector("input[onclick='ajaxInfoHS()']")

    def imgArrowType(self, number):
        return self.driver.find_element_by_css_selector("div[class='type-hotSpots']")\
            .find_element_by_css_selector("img[src*='{}.png']".format(number))

#############################################################

    def choose_theme(self, number):
        """
        Choose theme by number [1..4]

        :param number: Ordinal number of shown themes
        :type number: int [1..4]
        """
        self.log.info("Execute method choose_theme with parameter number={}".format(number))
        scroll_element_to_center(self.driver, self.log, self.btnChangeTheme())
        time.sleep(3)
        self.btnChangeTheme().click()
        wait_until(lambda: check_if_elem_exist(lambda: self.imgThemeToSelect(number)), timeout=30)
        newTheme = self.imgThemeToSelect(number)
        themeSrc = newTheme.find_element_by_tag_name("img").get_attribute("src")
        newTheme.click()
        wait_until(lambda: "selected" in self.imgThemeToSelect(number).get_attribute("class"), timeout=5)
        self.log.screenshot("Theme is selected")
        self.btnSelectTheme().click()
        wait_until(lambda: self.btnChangeTheme().find_element_by_tag_name("img").get_attribute("src") == themeSrc, timeout=20)
        self.log.screenshot("Theme is updated")


    def _add_button_to_center_with_selenium(self, hotSpot):
        """
        Puts hotSpot or info in center of scene.

        :param hotSpot: True if hotSpot is added, False if info is added
        :type hotSpot: bool
        """
        self.log.info("Execute method _add_button_to_center")
        if hotSpot:
            button = self.btnHotSpot
        else:
            button = self.btnInfo
        scroll_element_to_center(self.driver, self.log, button())
        buttonSize = button().size
        ac = ActionChains(self.driver)
        time.sleep(3)
        ac.move_to_element_with_offset(button(), buttonSize["width"]/2, buttonSize["height"]/2).perform()
        time.sleep(3)
        ac.click_and_hold().perform()
        tourSize = self.tourImage().size
        time.sleep(3)
        scroll_element_to_viewPoint_with_selenium(self.driver, self.tourImage())
        time.sleep(1)
        move_mouse_to_middle_of_browser(self.log, self.driver)
        time.sleep(1)
        ac.move_to_element_with_offset(self.tourImage(), tourSize["width"]/2, tourSize["height"]/2).perform()
        ac.release().perform()
        time.sleep(1)
        self.log.screenshot("Button is added")

    def _add_button_to_center_pyautogui(self, hotSpot):
        """
        Puts hotSpot or info in center of scene.

        :param hotSpot: True if hotSpot is added, False if info is added
        :type hotSpot: bool
        """
        self.log.info("Execute method _add_button_to_center")
        if hotSpot:
            button = self.btnHotSpot
        else:
            button = self.btnInfo
        move_mouse_to_element(self.driver, self.log, button())
        time.sleep(1)
        pyautogui.mouseDown(duration=1)
        move_mouse_to_element(self.driver, self.log, self.tourImage())
        time.sleep(1)
        pyautogui.mouseUp(duration=1)
        time.sleep(1)
        self.log.screenshot("Button is added")


    def _add_info_data(self, title, detail, url, mode="set"):
        """
        After info button is added to scene, insert information.

        :param mode: Possible values are set or update
        :type mode: str
        """
        self.log.info("Execute method _add_info_data with parameters "
                      "title={}, detail={}, url={}".format(title, detail, url))
        send_text(self.inpInfoTitle(), title, mode)
        send_text(self.inpInfoDetail(), detail, mode)
        send_text(self.inpInfoUrl(), url, mode)
        self.log.screenshot("Information is added")
        self.btnSaveInfo().click()
        time.sleep(3)

    def get_hotspot_from_center(self):
        hotSpotFound = None
        for hotSpot in get_hotSpots(self.log, self.driver):
            try:
                hotSpotLocation = hotSpot.get_attribute("style")
                translate = hotSpotLocation.split("translate(")[1].split("px")[0]
                hotSpotLocationWidth = int(translate.split(".")[0])
                size = hotSpot.size
                tourSceneCenter = self.tourImage().size["width"]/2
                self.log.info("Check if hotspot with x location={} is on center={}".format(hotSpotLocationWidth, tourSceneCenter))
                if abs(abs(hotSpotLocationWidth + size["width"]/2) - tourSceneCenter) <= 5:  #allowed error of 5 pixels
                    self.log.screenshot("Hotspot is in center")
                    hotSpotFound = hotSpot
                    return hotSpot
            except Exception as ex:
                self.log.info(str(ex))
        if hotSpotFound is None:
            raise Exception("HotSpot is not in center")

    def rotate(self, right, clickNumber):
        """
        Rotate scene to right or left clickNumber of times.

        :param right: True for moving to right, False for moving to left
        :type right: bool
        :param clickNumber: Number of times to click on arrow
        :type clickNumber: int
        """
        time.sleep(2)
        self.log.info("Execute method rotate with parameters right={}, clickNumber={}".format(right, clickNumber))
        if clickNumber != 0:
            if right:
                button = self.btnRighRotate
            else:
                button = self.btnLeftRotate
            for i in range(clickNumber):
                time.sleep(1.5)
                wait_until(lambda: check_if_elem_exist(button), timeout=10)
                button().click()
                time.sleep(1.5)
        self.log.screenshot("Rotate is done")

    def rotate_scene(self, pixels, width):
        """
        Width is full picture size. Pixels are inside of full width. This method will rotate scene
        so that pixels are on center of scene.

        :param pixels: Move scene to center of this location
        :type pixels: int
        :param width: Full width of scene
        :type width: int
        :return: Info about rotate number and direction. If bool True direction is right, otherwise left.
         Rotate number is number of times to rotate.
        :rtype: bool, int
        """
        self.log.info("Execute method rotate_scene with parameters pixels={}, width={}".format(pixels, width))
        oneMove = int(width/36)      #36 is number of clicking on rotate for 360
        if width/2 > pixels:
            #move left
            moveForPixels = width/2 - pixels
            numberRotate = int(moveForPixels/oneMove)
            self.rotate(False, numberRotate)
            return False, numberRotate
        else:
            #move right
            moveForPixels = pixels - width/2
            numberRotate = int(moveForPixels/oneMove)
            self.rotate(True, numberRotate)
            return True, numberRotate

    def save_hotSpot(self):
        """
        After hotSpot is added to location click on save button.
        """
        self.log.info("Execute method save_hotSpot")
        self.btnSaveHotSpot().click()
        time.sleep(2)

    def publish(self):
        """
        Execute publish button
        """
        self.log.info("Execute method publish")
        self.btnPublish().click()
        time.sleep(2)

    def change_current_scene(self, title):
        """
        Change current scene by clicking on pictures with title.

        :param title: Scene to change to
        :type title: str
        """
        self.log.info("Execute method change_current_scene with title={}".format(title))
        self.wait_scene_load()
        self.driver.find_element_by_xpath("//h5[contains(text(),'{}')]".format(title)).click()
        self.wait_scene_load()
        scroll_element_to_center(self.driver, self.log, self.tourImage())
        self.log.screenshot("Current scene changed to {}".format(title))

    def wait_scene_load(self):
        """
        When scene is chosen wait for it to load
        """
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_css_selector("div[class='pnlm-load-box']")), timeout=30)
        wait = WebDriverWait(self.driver, 60)
        wait.until(expected_conditions.invisibility_of_element(self.driver.find_element_by_css_selector("div[class='pnlm-load-box']")))

    def pan_to_view(self):
        """
        Click on button panToView
        """
        self.log.info("Execute method pan_to_view")
        self.driver.execute_script("arguments[0].click();", self.btnPanToView())
        #self.click_on_element(self.btnPanToView)
        time.sleep(3)

    def insert_hotSpots(self, scenes):
        """
        Insert hotSpots that are defined in scenes

        :param scenes: Data for scenes
        :type scenes: list[Scenes]
        """
        self.log.info("Execute method insert_hotSpots with parameter scenes={}".format("".join(scenes.__repr__())))
        for scene in scenes:
            self.change_current_scene(scene.title)
            for hotSpot in scene.hotSpots:
                self.rotate_scene(hotSpot.location, scene.width)
                self.add_button_to_center()
                self._set_hotSpot_goingTo(hotSpot.goingToScene)
                self.save_hotSpot()
                self.pan_to_view()

    def add_button_to_center(self, hotSpot=True):
        if DriverData.driverName == "Firefox":
            self._add_button_to_center_with_selenium(hotSpot)
        elif DriverData.driverName == "Chrome":
            self._add_button_to_center_pyautogui(hotSpot)
        else:
            self._add_button_to_center_safari(hotSpot)

    def _add_button_to_center_safari(self, hotSpot):
        time.sleep(3)
        self.log.info("Execute method _add_button_to_center")
        if hotSpot:
            button = self.btnHotSpot
        else:
            button = self.btnInfo
        oneScrollPixels = self._get_hotSpot_scroll_pixels(hotSpot)

        scroll_element_to_center(self.driver, self.log, self.btnHotSpot())
        fromLocation = get_location(self.driver, self.btnHotSpot())
        toLocation = get_location(self.driver, self.tourImage())

        scrollToBottom = self.driver.execute_script("return window.pageYOffset") + int(
            self.driver.execute_script("return window.innerHeight")) - fromLocation["y"] - 25

        wantedX = toLocation["x"] + int(self.tourImage().size["width"] / 2)
        wantedY = toLocation["y"] + int(self.tourImage().size["height"] / 2)

        currentX = fromLocation["x"] + int(button().size["width"]/2) + 50+10-10
        currentY = fromLocation["y"] + int(button().size["height"]/2) + scrollToBottom + 40
        x = wantedX - currentX
        y = wantedY - currentY
        print("x: {}".format(x))
        print("y: {}".format(y))
        time.sleep(1)

        moveFor = toLocation["y"] + self.tourImage().size["height"] / 2 - (
                    self.driver.execute_script("return window.pageYOffset") + int(
                self.driver.execute_script("return window.innerHeight"))) + int(
            self.driver.execute_script("return window.innerHeight") / 2)
        print("moveFor {}".format(moveFor))

        numberOfMoves = int(moveFor / oneScrollPixels)
        print("numberOfmoves {}".format(numberOfMoves))
        print("scroll to bottom {}".format(scrollToBottom))
        ActionChains(self.driver).move_to_element(self.btnHotSpot()).click_and_hold().move_by_offset(0, scrollToBottom)\
            .move_by_offset(10, 0).move_by_offset(-10, 0).move_by_offset(x, y).click(self.btnHotSpot()).release().perform()


    def _get_hotSpot_scroll_pixels(self, hotSpot):
        if hotSpot:
            element = self.btnHotSpot()
        else:
            element = self.btnInfo()
        startHidenPixels = get_hidden_pixels(self.driver)
        scroll_element_to_center(self.driver, self.log, element)
        action_chains = ActionChains(self.driver)
        hiddenPixels = get_hidden_pixels(self.driver)
        fromLocation = get_location(self.driver, element)

        action_chains.move_to_element(element)
        action_chains.click_and_hold()
        scrollFor = self.driver.execute_script("return window.pageYOffset") + int(
            self.driver.execute_script("return window.innerHeight")) - fromLocation["y"] - 25
        print(scrollFor)
        print(type(scrollFor))
        action_chains.move_by_offset(0, scrollFor)
        #action_chains.move_by_offset(10, 0)

        # action_chains.move_by_offset(10, 0)
        # action_chains.move_by_offset(-10, 0)
        action_chains.move_by_offset(0, -scrollFor)
        action_chains.release()
        action_chains.perform()
        hiddenPixelsAfter = get_hidden_pixels(self.driver)
        scrolledPixels = hiddenPixelsAfter - hiddenPixels
        print("pixels {}".format(scrolledPixels))
        self.driver.execute_script("scroll(0,{})".format(startHidenPixels))
        return scrolledPixels

    def delete_hotSpot(self, scene, hotSpotLocation):
        """
        Delete hotSpot from scene where location is hotSpotLocation.

        :param scene: Scene to delete hotSpot from
        :type scene: Scene
        :param hotSpotLocation: Location in pixels
        :type hotSpotLocation: int
        """
        self.log.info("Execute method delete_hotSpot with parameter scene={}, "
                      "hotSpotLocation={}".format(scene, hotSpotLocation))
        self.change_current_scene(scene.title)
        self.rotate_scene(hotSpotLocation, scene.width)
        self.delete_hotSpotOrInfo_center()

    def _set_hotSpot_goingTo(self, title):
        """
        After hotSpot is moved to scene, chose going to scene.

        :param title: Title of scene for hotSpot to show
        :type title: str
        """
        self.log.info("Execute method _set_hotSpot_goingTo with parameter={}".format(title))
        self.driver.find_element_by_xpath("//select[@id='select-hotSpots']/option[text()='{}']"
                                          .format(title)).click()


    def open_menu_hotSpotOrInfo_center(self):
        self.get_hotspot_from_center().click()
        wait_until(lambda: check_if_elem_exist(self.btnDeleteHotSpot), timeout=10)
        self.log.screenshot("Clicked on hotspot")

    def edit_hotSpot_center(self):
        self.log.info("Execute method edit_hotSpot_center")
        self.open_menu_hotSpotOrInfo_center()
        self.btnEditHotSpot().click()
        time.sleep(1)
        self.log.info("Edit hotspot clicked")
        action_chains = ActionChains(self.driver)
        scroll_element_to_center(self.driver, self.log, self.get_hotspot_from_center())
        move_mouse_to_middle_of_browser(self.log, self.driver)
        action_chains.drag_and_drop_by_offset(self.get_hotspot_from_center(), 5, 0).perform()
        time.sleep(1)
        self.log.screenshot("Edit for hotSpot is opened")

    def edit_hotSpot_goingTo(self, title):
        """
        After hotSpot is moved to scene, chose going to scene.

        :param title: Title of scene for hotSpot to show
        :type title: str
        """
        self.log.info("Execute method _set_hotSpot_goingTo with parameter={}".format(title))
        self.driver.find_element_by_xpath("//select[@id='edit-select-hotSpots']/option[text()='{}']"
                                          .format(title)).click()

    def save_edited_hotSpot(self):
        """
        After hotSpot is added to location click on save button.
        """
        self.log.info("Execute method save_hotSpot")
        self.btnSaveEditedHotSpot().click()
        time.sleep(2)

    def goTo_hotSpot_center(self):
        """
        Click on goTo in hotspot menu
        """
        self.open_menu_hotSpotOrInfo_center()
        self.log.info("Clicked on hotspot")
        self.btnGoToHotSpot().click()
        scroll_element_to_center(self.driver, self.log, self.tourImage())
        time.sleep(1)
        self.log.screenshot("GoTo hotspot clicked")
        self.wait_scene_load()
        self.log.screenshot("Moved to another scene")

    def choose_arrow(self, number):
        """
        Choose arrow type when adding or editing hotSpot.

        :param number: Number form 1 to 9
        :type number: int
        """
        self.log.info("Execute method choose_arrow with paramter number={}".format(number))
        self.imgArrowType(number).click()
        time.sleep(1)


    def add_info_button_center(self, title, name, url):
        """
        Add info button on center of tour and puts information.
        """
        self.log.info("Execute method add_info_button_center with parameters "
                      "title={}, name={}, url={}".format(title, name, url))
        self.add_button_to_center(hotSpot=False)
        self._add_info_data(title, name, url)
        self.log.info("Method add_info_button_center finished")

    def edit_info_button_center(self, title, name, url):
        """
        Edit info button on center of tour and puts information.
        """
        self.log.info("Execute method edit_info_button_center with parameters "
                      "title={}, name={}, url={}".format(title, name, url))
        action_chains = ActionChains(self.driver)
        self.open_menu_hotSpotOrInfo_center()
        time.sleep(2)
        action_chains.click(self.divHotSpotMenu().find_element_by_css_selector("a[onclick*='onInfoEdit']")).perform()
        time.sleep(2)
        scroll_element_to_center(self.driver, self.log, self.get_hotspot_from_center())
        move_mouse_to_middle_of_browser(self.log, self.driver)
        action_chains.drag_and_drop_by_offset(self.get_hotspot_from_center(), 5, 0).perform()
        time.sleep(1)
        self._add_info_data(title, name, url, "update")



    def delete_hotSpotOrInfo_center(self):
        """
        Delete hotSpot or info, depending what is on center of tour
        """
        self.log.info("Execute method delete_hotSpotOrInfo_center")
        time.sleep(1)
        self.open_menu_hotSpotOrInfo_center()
        self.log.screenshot("Click on delete hotspot")
        self.btnDeleteHotSpot().click()
        time.sleep(1)
        try:
            alert = self.driver.switch_to.alert
        except Exception as es:
            self.driver.log.info("First try to delete button not succeeded")
            self.btnDeleteHotSpot()
            alert = self.driver.switch_to.alert
        alert.accept()
        try:
            self.get_hotspot_from_center()
            raise Exception("Hotspot not deleted")
        except Exception as ex:
            pass
        self.log.screenshot("Hotspot is deleted")
