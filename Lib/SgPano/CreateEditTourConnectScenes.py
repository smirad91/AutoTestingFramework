"""
Class for manipulating with page https://sgpano.com/connect-scenes/
"""

import pyautogui
from selenium_move_cursor.MouseActions import move_to_element_chrome
from selenium.webdriver import ActionChains
import time
from Lib.common.CommonAction import CommonAction, get_hotSpots, move_mouse_to_element
from Lib.common.Log import Log
from Lib.common.NonAppSpecific import scroll_element_to_center, check_if_elem_exist, send_text, \
    get_location, get_hidden_pixels, \
    scroll_element_to_viewpoint_top
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

    def btnZoomOut(self):
        return self.driver.find_element_by_css_selector("img[src*='minus.svg']")

    def tourImage(self):
        return self.driver.find_element_by_class_name("pnlm-dragfix")

    def btnRighRotate(self):
        return self.driver.find_element_by_css_selector("img[src*='right-arrow.svg']")

    def btnUpRotate(self):
        return self.driver.find_element_by_css_selector("img[src*='up-arrow.svg']")

    def btnDownRotate(self):
        return self.driver.find_element_by_css_selector("img[src*='down-arrow.svg']")

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
        return self.driver.find_element_by_css_selector("a[class='button-changetheme']").find_element_by_tag_name("img")

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
        wait_until(lambda: check_if_elem_exist(self.btnChangeTheme), timeout=10)
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
        wait_until(lambda: self.btnChangeTheme().get_attribute("src") == themeSrc, timeout=20)
        self.log.screenshot("Theme is updated")

    def add_button_to_center(self, hotSpot=True):
        time.sleep(1)
        wait_until(lambda: "none" in self.driver.find_element_by_id("themeLabelHide").get_attribute("style"), timeout=30)
        if DriverData.driverName == "Firefox":
            self._add_button_to_center_firefox(hotSpot)
        elif DriverData.driverName == "Chrome":
            self._add_button_to_center_chrome(hotSpot)
        elif DriverData.driverName == "Safari":
            self._add_button_to_center_safari(hotSpot)

    def _add_button_to_center_firefox(self, hotSpot):
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
        #scroll_element_to_viewPoint_with_selenium(self.driver, self.tourImage())
        scroll_element_to_viewpoint_top(self.log, self.driver, self.tourImage())
        time.sleep(1)
        move_mouse_to_middle_of_browser(self.log, self.driver)
        time.sleep(1)
        ac.move_to_element_with_offset(self.tourImage(), tourSize["width"]/2, tourSize["height"]/2).perform()
        ac.release().perform()
        time.sleep(1)
        self.log.screenshot("Button is added")

    def _add_button_to_center_chrome(self, hotSpot):
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

        moveFor = toLocation["y"] + self.tourImage().size["height"] / 2 - (
                self.driver.execute_script("return window.pageYOffset") + int(
            self.driver.execute_script("return window.innerHeight"))) + int(
            self.driver.execute_script("return window.innerHeight") / 2)
        # print("moveFor {}".format(moveFor))
        numberOfMoves = int(moveFor / oneScrollPixels)

        wantedX = toLocation["x"] + int(self.tourImage().size["width"] / 2)
        wantedY = toLocation["y"] + int(self.tourImage().size["height"] / 2)

        currentX = fromLocation["x"] + int(button().size["width"] / 2)
        if numberOfMoves % 2 != 0:
            currentX += 10
        currentY = fromLocation["y"] + int(
            button().size["height"] / 2) + scrollToBottom + oneScrollPixels * numberOfMoves
        x = wantedX - currentX
        y = wantedY - currentY
        # print("x: {}".format(x))
        # print("y: {}".format(y))
        time.sleep(1)
        # print("numberOfmoves {}".format(numberOfMoves))
        # print("scroll to bottom {}".format(scrollToBottom))
        ac = ActionChains(self.driver)
        ac.move_to_element(self.btnHotSpot()).click_and_hold()

        self.drag_with_hotspot_safari(ac, scrollToBottom, numberOfMoves, x, y)

        ActionChains(self.driver).release().perform()

    def _get_hotSpot_scroll_pixels(self, hotSpot):
        """
        For how many pixels to move hotSpot so that scroll is activated

        :param hotSpot: HotSpot of info button. True if hotSpot.
        :type hotSpot: bool
        :return: Pixels to scroll for
        """
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
        #print(scrollFor)
        #print(type(scrollFor))
        action_chains.move_by_offset(0, scrollFor)
        #action_chains.move_by_offset(10, 0)

        # action_chains.move_by_offset(10, 0)
        # action_chains.move_by_offset(-10, 0)
        action_chains.move_by_offset(0, -scrollFor)
        action_chains.release()
        action_chains.perform()
        hiddenPixelsAfter = get_hidden_pixels(self.driver)
        scrolledPixels = hiddenPixelsAfter - hiddenPixels
        #print("pixels {}".format(scrolledPixels))
        self.driver.execute_script("scroll(0,{})".format(startHidenPixels))
        return scrolledPixels

    def drag_with_hotspot_safari(self, act, scrollToBottom, numberOfMoves, x, y):
        """
        Drag hotspot in safari with action chains

        :param act: ActionChains
        :param scrollToBottom: Pixels to scroll hotSpot so that scroll is activated
        :param numberOfMoves: Number of moves to get tour on center
        :param x: X location on center of tour
        :param y: Y location on center of tour
        """
        act.move_by_offset(0, scrollToBottom)
        moveToSide = 10
        for i in range(numberOfMoves):
            act.move_by_offset(moveToSide,0)
            moveToSide *= -1
        act.move_by_offset(x,y)
        act.perform()
        #return moveToSide

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

    def get_hotspot_from_center(self, center=True):
        """
        Return hotspot if on center or raise exception
        """
        hotSpotFound = None
        for hotSpot in get_hotSpots(self.log, self.driver):
            try:
                hotSpotLocation = hotSpot.get_attribute("style")
                translate = hotSpotLocation.split("translate(")[1].split("px")[0]
                hotSpotLocationWidth = int(translate.split(".")[0])
                size = hotSpot.size
                tourSceneCenter = self.tourImage().size["width"]/2
                self.log.info("Check if hotspot with x location={} is on center={}".format(hotSpotLocationWidth, tourSceneCenter))
                limit = 50
                if (hotSpotLocationWidth > tourSceneCenter-limit and hotSpotLocationWidth< tourSceneCenter+limit):  #allowed error of 50 pixels
                    self.log.screenshot("Hotspot is in center")
                    hotSpotFound = hotSpot
                    return hotSpot
            except Exception as ex:
                self.log.info(str(ex))
        if hotSpotFound is None:
            raise Exception("HotSpot is not in center")

    def get_hotspot_closer_to_center(self, center=True):
        """
        Return hotspot if on center or raise exception
        """
        hotSpotFound = None
        for hotSpot in get_hotSpots(self.log, self.driver):
            try:
                hotSpotLocation = hotSpot.get_attribute("style")
                translate = hotSpotLocation.split("translate(")[1].split("px")[0]
                hotSpotLocationWidth = int(translate.split(".")[0])
                size = hotSpot.size
                tourSceneCenter = self.tourImage().size["width"]/2
                self.log.info("Check if hotspot with x location={} is on center={}".format(hotSpotLocationWidth, tourSceneCenter))
                limit = 50
                if (hotSpotLocationWidth > tourSceneCenter-limit and hotSpotLocationWidth< tourSceneCenter+limit):  #allowed error of 50 pixels
                    self.log.screenshot("Hotspot is in center")
                    hotSpotFound = hotSpot
                    return hotSpot
            except Exception as ex:
                self.log.info(str(ex))
        if hotSpotFound is None:
            raise Exception("HotSpot is not in center")

    def rotate(self, right, clickNumber, useArrows):
        """
        Rotate scene to right or left clickNumber of times.

        :param right: True for moving to right, False for moving to left
        :type right: bool
        :param clickNumber: Number of times to click on arrow
        :type clickNumber: int
        """
        self.log.info("Execute method rotate with parameters right={}, clickNumber={}".format(right, clickNumber))
        if clickNumber != 0:
            if not useArrows:
                if DriverData.driverName == "Chrome" and DriverData.mobile is False:
                    for i in range(clickNumber):
                        time.sleep(5)
                        move_to_element_chrome(self.driver, self.tourImage(), 100)
                        pyautogui.mouseDown()
                        #moveFor = int(int(self.tourImage().size["width"]) / 58)
                        moveFor = int(int(self.tourImage().size["width"]) / 8)
                        if right:
                            pyautogui.moveRel(moveFor * -1, 0, 1)
                        else:
                            pyautogui.moveRel(moveFor, 0, 1)
                        pyautogui.mouseUp()
                        time.sleep(5)
                else:
                    for i in range(clickNumber):
                        time.sleep(5)
                        ac = ActionChains(self.driver)
                        ac.move_to_element(self.tourImage())
                        ac.click_and_hold()
                        #moveFor = int(int(self.tourImage().size["width"])/58)
                        moveFor = int(int(self.tourImage().size["width"]) / 8)
                        if right:
                            ac.move_by_offset(moveFor*-1, 0)
                        else:
                            ac.move_by_offset(moveFor, 0)
                        ac.release()
                        ac.perform()
                        time.sleep(5)
            else:
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

    def rotate2(self, move, useArrows, view):
        """
        Rotate scene to right or left clickNumber of times.

        :param move: List of strings where to move. Order is important. Example ["left:2","right:5","up:1","down:1"]
        :type move: list
        """
        self.log.info("Execute method rotate with parametersssssssss move={}".format(move))
        for move_to in move:
            move_number = move_to.split(":")
            move_where = move_number[0]
            move_number = int(move_number[1])
            if not view:
                self.move(move_where, move_number, useArrows, view)
            else:
                self.view_tour(move_where, move_number)
        self.log.screenshot("Rotate is done")

    def where_to_move_edit_and_view(self):
        self.log.info("Execute method _check_hotSpot_on_view")
        for hotSpot in get_hotSpots(self.log, self.driver):
            try:
                hotSpotLocation = hotSpot.get_attribute("style")
                translate = hotSpotLocation.split("translate(")[1].split("px")[0]
                hotSpotLocationWidth = int(translate.split(".")[0])
                size = hotSpot.size
                browserX = self.tourImage().size["width"]
                self.log.info("Check if hotspot with x location={} is on view={}".format(hotSpotLocationWidth, browserX))
                if hotSpotLocationWidth>0 and browserX / 2 > hotSpotLocationWidth - 125 and browserX / 2 > hotSpotLocationWidth + 175:
                    self.log.screenshot("Hotspot is on center")
                    return (abs(int(hotSpotLocationWidth - 125 - browserX / 2)),
                            abs(int(hotSpotLocationWidth + 175 - browserX / 2)))  # desno, levo

                # if browserX/2 > hotSpotLocationWidth-125 and browserX/2 > hotSpotLocationWidth+175:
                #     self.log.screenshot("Hotspot is on center")
                #     return (abs(int(hotSpotLocationWidth-125-browserX/2)), abs(int(hotSpotLocationWidth+175-browserX/2)))#desno, levo
            except:
                pass
        return (0,0)

    def view_tour(self, where, number):
        #if DriverData.mobile is True and "Portrait" in DriverData.orientation:
        number = number*2
        for i in range(number):
            self.log.screenshot("iiii: {}".format(i))
            time.sleep(2)
            moveForX = int(int(self.tourImage().size["width"]) / 8)
            moveForY = int(int(self.tourImage().size["height"]) / 8)
            ac = ActionChains(self.driver)
            if not self._check_hotSpot_on_view():
                self.log.screenshot("nije na centru")
                ac.move_to_element(self.tourImage())
            else:
                if i == 0:
                    ac.move_to_element(self.tourImage())
                    self.log.info("pomeri za 5 dole")
                    hs_loc = self.where_to_move_edit_and_view()
                    print(hs_loc)
                    print(hs_loc[0])
                    print(type(hs_loc))
                    print(type(hs_loc[0]))
                    if where =="right":
                        ac.move_by_offset(-1 * hs_loc[0],0)
                    elif where == "left":
                        ac.move_by_offset(hs_loc[1], 0)
                else:
                    break
            # if self.get_hotspot_location():
            #     ac.move_by_offset()
            self.log.screenshot("nastavio posle brejk")
            ac.click_and_hold()

            if where == "right":
                ac.move_by_offset(moveForX * -1, 0)
            elif where == "left":
                ac.move_by_offset(moveForX, 0)
            elif where == "up":
                ac.move_by_offset(0, moveForY * -1)
            elif where == "down":
                ac.move_by_offset(0, moveForY)
            ac.release()
            ac.perform()
            time.sleep(2)
            self.log.screenshot("prvi je pomeri na centar izvrsenoooooooooo jedno pomeranje")


    def is_hs_on_center(self):
        try:
            for hotSpot in get_hotSpots(self.log, self.driver):
                hotSpotLocation = hotSpot.get_attribute("style")
                translate = hotSpotLocation.split("translate(")[1].split("px")[0]
                hotSpotLocationWidth = int(translate.split(".")[0])
                size = hotSpot.size
                centerOfBrowser = self.driver.find_element_by_tag_name("body").size["width"]/2
                self.log.info("Check if hotspot with x location={} is on center={}".format(hotSpotLocationWidth, centerOfBrowser))
                if abs(self.tourImage().size["width"]/2 - hotSpotLocationWidth) <= 55:
                    return True
                #y check
        except:
            pass
        return False

    def _check_hotSpot_on_view(self):
        """
        Check if hotSpot is in center of view. And it shows to scene title=goingToScene. If hotSpot is not found
        or hotSpot is not in center exception is raised.

        :param goingToScene: Scene title that hotSpot should point
        :type goingToScene: str
        """
        self.log.info("Execute method _check_hotSpot_on_view")
        for hotSpot in get_hotSpots(self.log, self.driver):
            try:
                hotSpotLocation = hotSpot.get_attribute("style")
                translate = hotSpotLocation.split("translate(")[1].split("px")[0]
                hotSpotLocationWidth = int(translate.split(".")[0])
                size = hotSpot.size
                #browserX = self.driver.find_element_by_tag_name("body").size["width"]
                browserX = self.tourImage().size["width"]
                self.log.info("Check if hotspot with x location={} is on view={}".format(hotSpotLocationWidth, browserX))
                #if browserX - (hotSpotLocationWidth + size["width"]) > 0 and browserX - (hotSpotLocationWidth + size["width"]) < browserX:
                if hotSpotLocationWidth >= 0 and hotSpotLocationWidth <= browserX:
                    self.log.screenshot("Hotspot is on view")
                    return True
            except:
                pass
        return False


    def move(self, where, number, useArrows, view):
        if useArrows:
            for i in range(number):
                if where == "right":
                    self.btnRighRotate().click()
                elif where == "left":
                    self.btnLeftRotate().click()
                elif where == "up":
                    self.btnDownRotate().click()
                elif where == "down":
                    self.btnLeftRotate().click()
        else:
            for i in range(number):
                self.log.screenshot("iiii: ",i)
                time.sleep(2)
                moveForX = int(int(self.tourImage().size["width"]) / 8)
                moveForY = int(int(self.tourImage().size["height"]) / 8)
                try:
                    self.get_hotspot_from_center()
                except:
                    ac = ActionChains(self.driver)
                    ac.move_to_element(self.tourImage())
                    if where == "right":
                        ac.move_by_offset(moveForX, 0)
                    elif where == "left":
                        ac.move_by_offset(-moveForX, 0)
                    elif where == "up":
                        ac.move_by_offset(0, moveForY)
                    elif where == "down":
                        ac.move_by_offset(0, -moveForY)
                    ac.click_and_hold()

                    if where == "right":
                        ac.move_by_offset(moveForX * -1, 0)
                    elif where == "left":
                        ac.move_by_offset(moveForX, 0)
                    elif where == "up":
                        ac.move_by_offset(0, moveForY * -1)
                    elif where == "down":
                        ac.move_by_offset(0, moveForY)
                    ac.release()
                    ac.perform()
                    time.sleep(2)
                    self.log.screenshot("prvi je pomeri na centar izvrsenoooooooooo jedno pomeranje")


    def get_number_rotate(self, pixels, width):
        oneMove = int(width / 36)  # 36 is number of clicking on rotate for 360
        if width / 2 > pixels:
            # move left
            moveForPixels = width / 2 - pixels
            numberRotate = int(moveForPixels / oneMove)
            return False, numberRotate
        else:
            # move right
            moveForPixels = pixels - width / 2
            numberRotate = int(moveForPixels / oneMove)
            return True, numberRotate


    def rotate_scene(self, pixels, width, useArrows=True, viewTour=False, up=False, down=False):
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
            rotate = ["left:{}".format(numberRotate)]
            if up!=0:
                rotate.append("up:{}".format(up))
            elif down:
                rotate.append("down:{}".format(down))
            print(rotate)
            self.rotate2(rotate, useArrows, viewTour)
            return False, numberRotate
        else:
            #move right
            moveForPixels = pixels - width/2
            numberRotate = int(moveForPixels/oneMove)
            rotate = ["right:{}".format(numberRotate)]
            if up:
                rotate.append("up:1")
            elif down:
                rotate.append("down:3")
            self.rotate2(rotate, useArrows, viewTour)
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
        self.driver.set_page_load_timeout(30)
        time.sleep(3)
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_class_name("pnlm-render-container").find_element_by_tag_name("canvas")), timeout=60)
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_css_selector("div[class='pnlm-load-box']")), timeout=30)
        wait_until(lambda: "inline" not in self.driver.find_element_by_css_selector("div[class='pnlm-load-box']").get_attribute('style'), timeout=60)


    def pan_to_view(self):
        """
        Click on button panToView
        """
        self.log.info("Execute method pan_to_view")
        self.driver.execute_script("arguments[0].click();", self.btnPanToView())
        #self.click_on_element(self.btnPanToView)
        time.sleep(3)

    def stop_rotate(self):
        self.rotate(False, 1, True)
        self.pan_to_view()

    def insert_hotSpots(self, scenes):
        """
        Insert hotSpots that are defined in scenes

        :param scenes: Data for scenes
        :type scenes: list[Scenes]
        """
        self.log.info("Execute method insert_hotSpots with parameter scenes={}".format("".join(scenes.__repr__())))
        for scene in scenes:
            self.change_current_scene(scene.title)
            self.stop_rotate()
            for hotSpot in scene.hotSpots:
                # self.add_button_to_center()
                # self._set_hotSpot_goingTo(hotSpot.goingToScene)
                # self.save_hotSpot()
                # hsCenter = self.get_hotspot_from_center()
                # print("pre {}".format(hsCenter.location))
                # for i in range(36):
                #     print(i)
                #     self.btnRighRotate().click()
                #     time.sleep(3)
                #     print("posle {}".format(hsCenter.location))
                # time.sleep(1000)
                self.rotate_scene(hotSpot.location, scene.width, useArrows=False, up=hotSpot.up, down=hotSpot.down)
                self.add_button_to_center()
                self._set_hotSpot_goingTo(hotSpot.goingToScene)
                self.save_hotSpot()
                self.pan_to_view()

    def rotate_scene_cursor(self, location, width):
        for i in range(7):
            time.sleep(10)
            self.half_rotate()

    def half_rotate(self):
        ac = ActionChains(self.driver)
        ac.move_to_element(self.tourImage())
        ac.click_and_hold()
        print(self.tourImage().size["width"] / 2)
        ac.move_by_offset(self.tourImage().size["width"] / 2, 0)
        ac.release()
        ac.perform()

    def full_rotate(self):
        ac = ActionChains(self.driver)
        ac.move_to_element(self.tourImage())
        ac.move_by_offset(-1 * self.tourImage().size["width"] / 2,0)
        ac.click_and_hold()
        print(self.tourImage().size["width"])
        ac.move_by_offset(self.tourImage().size["width"], 0)
        ac.release()
        ac.perform()

    def delete_hotSpot(self, scene, hotSpotLocation, center=True):
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
        self.stop_rotate()
        self.rotate_scene(hotSpotLocation, scene.width, False)
        self.delete_hotSpotOrInfo_center(True)

    def _set_hotSpot_goingTo(self, title):
        """
        After hotSpot is moved to scene, chose going to scene.

        :param title: Title of scene for hotSpot to show
        :type title: str
        """
        self.log.info("Execute method _set_hotSpot_goingTo with parameter={}".format(title))
        options = self.driver.find_element_by_xpath("//select[@id='select-hotSpots']")
        goingTo = self.driver.find_element_by_xpath("//select[@id='select-hotSpots']/option[text()='{}']"
                                          .format(title))
        scroll_element_to_center(self.driver, self.log, options)
        options.click()
        time.sleep(2)
        goingTo.click()
        time.sleep(2)


    def open_menu_hotSpotOrInfo_center(self):
        """
        Open menu of button in center of tour
        """
        time.sleep(5)
        self.get_hotspot_from_center().click()
        wait_until(lambda: check_if_elem_exist(self.btnDeleteHotSpot), timeout=10)
        self.log.screenshot("Clicked on hotspot")

    def open_menu_hotSpotOrInfo_on_view(self):
        """
        Open menu of button in center of tour
        """
        time.sleep(5)
        hotSpotFound = None
        for hotSpot in get_hotSpots(self.log, self.driver):
            try:
                hotSpotLocation = hotSpot.get_attribute("style")
                translate = hotSpotLocation.split("translate(")[1].split("px")[0]
                hotSpotLocationWidth = int(translate.split(".")[0])
                size = hotSpot.size
                tourSceneSize = self.tourImage().size["width"]
                self.log.info(
                    "Check if hotspot with x location={} is on view={}".format(hotSpotLocationWidth, tourSceneSize))
                limit = 50
                # if abs(abs(hotSpotLocationWidth + size["width"]/2) - tourSceneCenter) <= tourSceneCenter/2 and hotSpotLocationWidth>=0:  #allowed error of 20 pixels
                #     self.log.screenshot("Hotspot is in center")
                #     hotSpotFound = hotSpot
                #     return hotSpot
                if hotSpotLocationWidth >= 0 and hotSpotLocationWidth <= tourSceneSize:
                    self.log.screenshot("Hotspot is on view")
                    hotSpotFound = hotSpot
                    hotSpot.click()
            except Exception as ex:
                self.log.info(str(ex))
        if hotSpotFound is None:
            raise Exception("HotSpot is not in center")
        wait_until(lambda: check_if_elem_exist(self.btnDeleteHotSpot), timeout=10)
        self.log.screenshot("Clicked on hotspot")


    def edit_hotSpot_center(self):
        """"
        Edit hotSpot
        """
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
        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath("//select[@id='edit-select-hotSpots']/option[text()='{}']"
                                          .format(title)))
        # self.driver.find_element_by_xpath("//select[@id='edit-select-hotSpots']/option[text()='{}']"
        #                                   .format(title)).click()

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



    def delete_hotSpotOrInfo_center(self, center=True):
        """
        Delete hotSpot or info, depending what is on center of tour
        """
        self.log.info("Execute method delete_hotSpotOrInfo_center")
        time.sleep(1)
        if center:
            self.open_menu_hotSpotOrInfo_center()
        else:
            self.open_menu_hotSpotOrInfo_on_view()
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


