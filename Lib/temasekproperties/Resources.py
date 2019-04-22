import time

from Lib.common.Log import Log
from Lib.common.NonAppSpecific import check_if_elem_exist
from Lib.common.WaitAction import wait_until


class Resources:

    def __init__(self, driver):
        self.driver = driver
        self.log = Log(driver)

    def tblBooked(self):
        return self.driver.find_element_by_css_selector("table[class='table table-striped bookly-appointments-list dataTable no-footer dtr-inline']")

    def btnNext(self):
        return self.driver.find_element_by_css_selector("button[class='bookly-next-step bookly-js-next-step bookly-btn ladda-button']")

    def check_if_exist(self, listingName, bookDate):
        wait_until(lambda: check_if_elem_exist(self.tblBooked))
        all_booked = self.tblBooked().find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        for booked in all_booked:
            sections = booked.find_elements_by_tag_name("td")
            if bookDate in sections[0].text and listingName in sections[1].text:
                self.log.screenshot("Exists")
                return True
        self.log.screenshot("Does not exist!!!")
        return False

    def book(self, serviceName, selectionName):
        selectService = self.driver.find_element_by_css_selector("div[class='bookly-js-chain-item bookly-table bookly-box']")\
            .find_element_by_css_selector("select[class='bookly-select-mobile bookly-js-select-service']")
        for service in selectService.find_elements_by_tag_name("option"):
            if serviceName in service.text:
                service.click()
                break
        time.sleep(2)
        selectSelection = self.driver.find_element_by_css_selector("div[class='bookly-js-chain-item bookly-table bookly-box']")\
            .find_element_by_css_selector("select[class='bookly-select-mobile bookly-js-select-employee']")
        for selection in selectSelection.find_elements_by_tag_name("option"):
            if selectionName in selection.text:
                selection.click()
                break
        self.log.screenshot("Selected booking for {} and {}".format(serviceName, selectionName))

    def booking_steps(self):
        self.btnNext().click()
        wait_until(lambda: check_if_elem_exist(lambda: self.driver.find_element_by_css_selector("div[class='bookly-box']")))
        wait_until(lambda: "Below you can find a list of available time slots" in self.driver.find_element_by_css_selector("div[class='bookly-box']").text)
        self.log.screenshot("Opened 'Time'")
        self.driver.find_element_by_css_selector("div[class='bookly-column bookly-js-first-column']")\
            .find_element_by_css_selector("button[class='bookly-hour']").click()
        #wait_until(lambda: "Details" in self.active_booking_step())
        wait_until(lambda: self.active_booking_step("Details"))
        self.log.screenshot("'Details' opened")
        booking = self.driver.find_element_by_css_selector("div[class='bookly-box']").find_elements_by_tag_name("b")
        bookDate = booking[3].text
        bookTime = booking[2].text
        bookedFor = bookDate + " " + bookTime
        self.driver.find_element_by_css_selector("button[class='bookly-next-step bookly-js-next-step bookly-btn ladda-button']").click()
        #wait_until(lambda: "Done" in self.active_booking_step())
        wait_until(lambda: self.active_booking_step("Done"))
        self.log.screenshot("Booking is done")
        self.log.info("booked for {}".format(bookedFor))
        return bookedFor

    def active_booking_step(self, stepName):
        steps = self.driver.find_element_by_css_selector(
            "div[class='bookly-progress-tracker bookly-table']").find_elements_by_tag_name("div")
        for step in steps:
            if "active" in step.get_attribute("class"):
                if stepName in step.text:
                    return True
        return False
