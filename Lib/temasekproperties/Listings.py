import time
from Lib.common.CommonAction import CommonAction

from selenium.webdriver import ActionChains

from Lib.common.Log import Log
from Lib.common.NonAppSpecific import send_text, check_if_elem_exist, click_on_element_intercepted, wait_page_load
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

    def btnPayPal(self):
        return self.driver.find_element_by_css_selector("span[class='paypal-button-content']")

    def inpSearch(self):
        return self.driver.find_element_by_css_selector("input[placeholder='Search …']")



    def btnSearch(self):
        return self.driver.find_element_by_css_selector("input[name='_sf_submit']")

    def get_all_listings(self):
        root = self.driver.find_element_by_css_selector("div[class='edd_downloads_list edd_download_columns_3']")
        allDivs = root.find_elements_by_tag_name("div")
        allListing = []
        for div in allDivs:
            if div.get_attribute("class") == "edd_download" or \
                    div.get_attribute("class") == "edd_download download_bought":
                allListing.append(div)
        return allListing

    def change_page(self, page):
        self.log.info("Execute method change_page with parameter page={}".format(page))
        if page != 1:
            self.driver.get("https://temasekproperties.com/listings/?sf_paged={}".format(page))
        self.log.screenshot("Page opened")

    def open_listing_by_index(self, index):
        self.log.info("Execute method open_listing_by_index with parameter index={}".format(index))
        self.get_all_listings()[int(index)-1].find_element_by_tag_name("a").click()
        wait_page_load(self.driver)

    def purchase_listing(self, payment, email, firstName, lastName, payPalEmail, payPalPassword):
        self.log.info("Execute method purchase_listing")
        time.sleep(5)
        #formElement = self.driver.find_element_by_css_selector("form[id='edd_purchase_9273']") #edd_download_purchase_form edd_purchase_9273
        formElement = self.driver.find_element_by_css_selector("div[class='edd_price_options edd_single_mode']")
        purchases = formElement.find_elements_by_css_selector("span[class='edd_price_option_name']")
        for purchase in purchases:
            if purchase.text == payment:
                purchase.find_element_by_xpath('..').click()
                time.sleep(1)
                self.log.screenshot("Selected payment={}".format(payment))
                break
        self.aPurchase().click()
        time.sleep(5)
        self.aCheckout().click()
        send_text(self.inpEmail(), email, mode="update")
        send_text(self.inpFirstName(), firstName, mode="update")
        send_text(self.inpLastName(), lastName, mode="update")
        self.log.screenshot("Inserted email, firstname, lastname")
        self.btnFinalPurchase().click()
        wait_until(lambda: check_if_elem_exist(self.btnPayPal), 30)
        time.sleep(10)
        self.btnPayPal().click()
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_id("payment_type_paypal")), timeout=60)
        self.driver.find_element_by_id("payment_type_paypal").click()
        self.driver.find_element_by_css_selector("input[name='unified_login.x']").click()
        #paypal window is opened
        self.log.info("Add PayPal credentials")
        wait_until(lambda: check_if_elem_exist(self.inpPayPalEmail), timeout=60)
        send_text(self.inpPayPalEmail(), payPalEmail, mode="update")
        send_text(self.inpPayPalPass(), payPalPassword, mode="update")
        self.log.screenshot("Credentials for PayPal are entered")
        self.btnLogInPayPal().click()
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_css_selector("input[name='submit.x']")))
        self.driver.find_element_by_css_selector("input[name='submit.x']").click()
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_xpath(
            "//h1[contains(text(),'{}')]".format("Your purchase was successful"))))
        self.log.screenshot("Listing purchased")


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

    def search_for(self, searchFor):
        send_text(self.inpSearch(), searchFor)
        self.btnSearch().click()
        wait_page_load(self.driver)

    # def book(self, listingName):
    #     all_listings = self.get_all_listings()
    #     for listing in all_listings:
    #        if listingName in listing.find_element_by_css_selector("a[itemprop='url']").text:
    #            listing.find_element_by_tag_name("button").click()
    #            wait_until(lambda: "Service" in self.active_booking_step())
    #            break



