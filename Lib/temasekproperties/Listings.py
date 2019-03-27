import time

from Lib.common.Log import Log
from Lib.common.NonAppSpecific import send_text


class Listings:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def aPurchase(self):
        self.driver.find_element_by_css_selector("a[class='edd-add-to-cart button blue edd-submit edd-has-js']")

    def aCheckout(self):
        self.driver.find_element_by_css_selector("a[href='https://temasekproperties.com/checkout/']")

    def inpEmail(self):
        self.driver.find_element_by_css_selector("input[id='edd-email']")

    def inpFirstName(self):
        self.driver.find_element_by_css_selector("input[id='edd-first']")

    def inpLastName(self):
        self.driver.find_element_by_css_selector("input[id='edd-last']")

    def btnFinalPurchase(self):
        self.driver.find_element_by_id("edd-purchase-button")

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

    def purchase_listing(self, payment, email, firstName, lastName):
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
