import time

from Lib.common.CommonAction import CommonAction
from selenium.webdriver import ActionChains

from Lib.common.Log import Log
from Lib.common.NonAppSpecific import send_text, check_if_elem_exist
from Lib.common.WaitAction import wait_until


class Listings(CommonAction):

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def aPurchase(self):
        return self.driver.find_element_by_css_selector("a[class='edd-add-to-cart button blue edd-submit edd-has-js']")

    def aCheckout(self):
        return self.driver.find_element_by_css_selector("a[href='https://temasekproperties.com/checkout/']")
    def inpEmail(self):
        return self.driver.find_element_by_css_selector("input[id='edd-email']")

    def inpFirstName(self):
        return self.driver.find_element_by_css_selector("input[id='edd-first']")

    def inpLastName(self):
        return self.driver.find_element_by_css_selector("input[id='edd-last']")

    def btnFinalPurchase(self):
        return self.driver.find_element_by_id("edd-purchase-button")

    def aPlay(self):
        return self.driver.find_element_by_css_selector("a[id='button-play']")

    def canvas(self):
        return self.driver.find_element_by_tag_name("canvas")

    def ddlistFloor(self):
        return self.driver.find_element_by_css_selector("div[class='gui-floor hasHover open']")

    def lstFloor(self):
        return self.ddlistFloor().find_element_by_css_selector("div[class='container']")

    def btnFloor(self):
        return self.driver.find_element_by_css_selector("div[class*='gui-floor hasHover']").\
            find_element_by_css_selector("i[class='icon icon-dpad-up']")

    def get_all_listings(self):
        root = self.driver.find_element_by_css_selector("div[class='edd_downloads_list edd_download_columns_3']")
        allDivs = root.find_elements_by_tag_name("div")
        allListing = []
        for div in allDivs:
            print(div.get_attribute("class"))
            if div.get_attribute("class") == "edd_download":
                allListing.append(div)
        print(len(allListing))
        return allListing

    def open_listing_by_index(self, index):
        return self.get_all_listings()[index-1].find_element_by_tag_name("a").click()

    def purchase_listing(self, payment, email, firstName, lastName, payPalEmail, payPalPassword):
        #formElement = self.driver.find_element_by_css_selector("form[id='edd_purchase_9273']") #edd_download_purchase_form edd_purchase_9273
        formElement = self.driver.find_element_by_css_selector("div[class='edd_price_options edd_single_mode']")
        purchases = formElement.find_elements_by_css_selector("span[class='edd_price_option_name']")
        for purchase in purchases:
            if purchase.text == payment:
                purchase.find_element_by_xpath('..').click()
                break
        self.aPurchase().click()
        time.sleep(5)
        self.aCheckout().click()
        send_text(self.inpEmail(), email)
        send_text(self.inpFirstName(), firstName)
        send_text(self.inpLastName(), lastName)
        self.btnFinalPurchase().click()
        #paypal window is opened
        self.pay_pal(payPalEmail, payPalPassword, 60)

    def play(self):
        self.driver.switch_to.frame(self.driver.find_element_by_id("frame_me"))
        time.sleep(5)
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_css_selector("a[id='button-play']")), timeout=60)
        self.aPlay().click()

        # ac = ActionChains(self.driver)
        # ac.click(self.aPlay())
        # ac.perform()
        #self.driver.execute_script("arguments[0].click();", self.aPlay())
        wait_until(lambda: "display: none;" in self.driver.find_element_by_id("gui-loading").get_attribute("style"), timeout=60)

    def moveListing(self, numberOfMoves, right=True):
        # for i in range(numberOfMoves):
        #     time.sleep(6)
        #     ac = ActionChains(self.driver)
        #     ac.move_to_element(self.canvas())
        #     ac.move_by_offset(100, 0)
        #     ac.move_by_offset(100, 0)
        #     ac.click_and_hold()
        #     if right:
        #         ac.move_by_offset(-1*int(self.canvas().size["width"]/8), 0)
        #     else:
        #         ac.move_by_offset(int(self.canvas().size["width"]/8), 0)
        #     ac.release()
        #     ac.perform()
        #     time.sleep(2)
        #     self.log.screenshot("nakon pomeranje")
        for i in range(numberOfMoves):
            time.sleep(6)
            ActionChains(self.driver).move_to_element(self.canvas()).perform()
            ActionChains(self.driver).click_and_hold().perform()
            if right:
                ActionChains(self.driver).move_by_offset(-1*int(self.canvas().size["width"]/8), 0).perform()
            else:
                ActionChains(self.driver).move_by_offset(int(self.canvas().size["width"]/8), 0).perform()
            ActionChains(self.driver).release().perform()
            time.sleep(2)
            self.log.screenshot("Listing moved")

    def choose_floor(self, floor):
        try:
            time.sleep(5)
            wait_until(lambda: check_if_elem_exist(self.btnFloor), timeout=60)
            self.btnFloor().click()
            wait_until(lambda: check_if_elem_exist(self.ddlistFloor), timeout=10)
            self.lstFloor().find_element_by_css_selector("div[data-index='{}']".format(floor-1)).click()
            wait_until(lambda: not check_if_elem_exist(self.ddlistFloor), timeout=10)
            return True
        except Exception as ex:
            return False