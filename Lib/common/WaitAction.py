"""
Wait mechanisms for action in browser to finish. For example when clicked on upload photos, it can take a while,
so we need to wait for action to finish.
"""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def wait_until(somepredicate, timeout=60, period=1, errorMessage="Timeout expired"):
    """
    Somepredicate is function that returns True or False. This function is executed every for period during
    timeout. When somepredicate return True wait is done. If somepredicate don't return True during timeout,
    exception is raised.

    :param somepredicate: Function that return True of False
    :type somepredicate: func
    :param timeout: Timeout to wait
    :type timeout: int
    :param period: Execute function for every period seconds
    :type period: float
    :return:
    """
    mustend = time.time() + timeout
    value = False
    while time.time() < mustend:
        try:
            value = somepredicate()
        except Exception as ex:
            #print(ex)
            pass
        if value:
            return True
        time.sleep(period)
    raise Exception(errorMessage)

def wait_element_visible(driver, cssSelector, timeout=500):
    """
    Wait for element with cssSelector to be shown on browser.
    
    :param driver: Driver
    :type driver: WebDriver
    :param cssSelector: Css selector form
    :type cssSelector: str
    :return: 
    """""
    wait = WebDriverWait(driver, timeout)
    wait.until(expected_conditions.visibility_of_element_located(
        (By.CSS_SELECTOR, cssSelector)))