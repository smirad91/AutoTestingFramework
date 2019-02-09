"""
Class used to create logs with messages and screenshots in Logs folder
"""
import logging
import os
import sys
from os import path
import atexit
import traceback

import pyautogui

from Lib.common.NonAppSpecific import close_driver


class Log:

    createdLog = 0
    screenshotNumber = 0
    testLogFolderPath = ""
    driver = None

    def __init__(self, driver):
        """
        Creates Log instance with given driver. (Driver is used to generate screenshots)
        :param driver: Driver
        :type driver: WebDriver
        """
        if Log.createdLog == 0:
            Log.driver = driver
            logName = path.basename(sys.modules['__main__'].__file__).split('.')[0]
            logFolderPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         os.pardir, os.pardir, "Logs")
            if any(x.startswith(logName) for x in os.listdir(logFolderPath)):
                logFolderNumbers = []
                for x in os.listdir(logFolderPath):
                    if x.startswith(logName):
                        try:
                            logFolderNumbers.append(int(x.split("-")[1]))
                        except:
                            pass
                try:
                    newNumber = max(logFolderNumbers)
                except:
                    newNumber = 0
                newTestLogFolderPath = newNumber + 1
                testLogFolderPath = os.path.join(logFolderPath, logName + "-" + str(newTestLogFolderPath))
                os.mkdir(testLogFolderPath)
            else:
                testLogFolderPath = os.path.join(logFolderPath, logName)
                os.mkdir(testLogFolderPath)
            Log.testLogFolderPath = testLogFolderPath
            self.fileName = os.path.join(testLogFolderPath, logName+".html")
            logging.basicConfig(filename=self.fileName, level=logging.INFO, format='%(message)s')
            Log.createdLog = 1
            atexit.register(self.exit_handler)

    def info(self, msg):
        """
        Log info message in log

        :param msg: Message to log
        :type msg: str
        """
        logging.getLogger().info("<p>"+msg+"</p>")

    def screenshot(self, msg, fullScreen=False):
        """
        Log screenshot with message

        :param msg: Message to log
        :type msg: str
        """
        screenshotName = str(Log.screenshotNumber) + ".png"
        picturePath = os.path.join(Log.testLogFolderPath, screenshotName)
        Log.screenshotNumber += 1
        if fullScreen:
            pyautogui.screenshot(picturePath)
        else:
            Log.driver.save_screenshot(picturePath)
        logging.getLogger().info("<p><a href='{}'><img src='{}' height='150px' width='200px'></img></a><br>{}</p>".format(screenshotName, screenshotName,msg))


    def exit_handler(self):
        """
        Mechanism that is going to be used when test is finished. Adding screenshot at the end of log
         and logs exception if happened.
        """
        if hasattr(sys, 'last_type'):
            self.screenshot("", True)
            self.screenshot("".join(traceback.format_exception(sys.last_type, sys.last_value, sys.last_traceback)))
        else:
            self.screenshot("Test ended successfully")
        close_driver(self.driver)
