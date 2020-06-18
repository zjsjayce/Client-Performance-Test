# -*- coding: utf-8 -*-

import threading
import time

import Utils.logger as logger
from appium import webdriver
import os

from casePackage.utils import apptool
from ConfigParser import ConfigParser

from selenium.common.exceptions import WebDriverException, NoSuchElementException
from urllib3.exceptions import MaxRetryError

LOGGING = logger.get_logger(__name__)
def getConfig(file='config.ini'):
    cf = ConfigParser()
    file_path = os.path.join(os.path.join(os.path.abspath('..'), 'config'), file)
    if not os.path.exists(file_path):
        file_path = os.path.join(os.path.join(os.getcwd(), 'casePackage/config'), file)
    if not os.path.exists(file_path):
        file_path = os.path.join('home/jenkins/Source/LRP/lrp/casePackage/config', file)
    cf.read(file_path)
    return cf


def getDriver(app, file='config.ini', device=None, installing=False):
    cf = getConfig(file)
    desired_caps = {}
    desired_caps["platformName"] = cf.get("init", "platformName")
    if device:
        desired_caps["platformVersion"] = cf.get(device, 'platformVersion')
        desired_caps["deviceName"] = cf.get(device, 'deviceName')
    else:
        desired_caps["platformVersion"] = cf.get('init', 'platformVersion')
        desired_caps["deviceName"] = cf.get('init', 'deviceName')
    desired_caps['noReset'] = True
    desired_caps["unicodeKeyboard"] = False
    desired_caps["resetKeyBoard"] = False
    desired_caps["appPackage"] = cf.get(app, 'appPackage')
    desired_caps["appActivity"] = cf.get(app, 'appActivity')
    desired_caps["noSign"] = True
    try:
        desired_caps["appWaitActivity"] = cf.get(app, 'appWaitActivity')
    except:
        pass

    desired_caps["newCommandTimeout"] = 6000
    # desired_caps["commandTimeouts"] = 20
    desired_caps["automationName"] = "UiAutomator2"
    desired_caps["udid"] = cf.get(device, 'deviceName')
    desired_caps["systemPort"] = eval(cf.get(device, 'systemPort'))
    desired_caps["noReset"] = True
    desired_caps["skipUnlock"] = True
    desired_caps["app"] = os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), ".."), ".."),
                                    cf.get(app, 'app')))
    webdriver_url = 'http://localhost:' + cf.get(device, 'appium_server_port') + '/wd/hub'
    # webdriver_url = 'http://localhost:4723/wd/hub'
    driver = webdriver.Remote(webdriver_url, desired_caps)
    driver.implicitly_wait(2)
    if installing:
        l = listener(desired_caps["deviceName"], app, '立即删除/继续安装', driver, True)
        l.start()
        return l, driver
    if app == apptool.TOUTIAO:
        l = listener(desired_caps["deviceName"], app, '始终允许/同意', driver)
        l.start()
    else:
        l = listener(desired_caps["deviceName"], app, '同意', driver)
        l = listener(desired_caps["deviceName"], app, '允许', driver)
        l.start()
    # if app == apptool.NETEASE:
    #     l = listener(desired_caps["deviceName"], app, '允许', driver)
    #     l.start()
    return l, driver

class listener(threading.Thread):
    def __init__(self, device, app, text, driver, when_install = False):
        threading.Thread.__init__(self)
        self.device = device
        self.app = app
        self.text = str(text).split("/")
        self.driver = driver
        self.when_install = when_install
        self.is_stopped = False

    def stop(self):
        self.is_stopped = True

    def run(self):
        apptools = apptool.apptool(self.app, self.device, ' ')
        apptools.startApp()
        while not self.is_stopped:
            for k in self.text:
                if k == "同意" or k == "同意并进入":
                    xpath_id = "//android.widget.TextView[@text='" + k + "']"
                else:
                    xpath_id = "//android.widget.Button[contains(@text, '" + k + "')]"
                try:
                    element = self.driver.find_element_by_xpath(xpath_id)
                    if element:
                        element.click()
                        # self.driver.tap([(element.location['x'], element.location['y'])])
                except Exception, e:
                    if isinstance(e, NoSuchElementException):
                        pass
                    else:
                        # In order to log all exception and don't miss any, didn't use "except MaxRetruError"
                        LOGGING.exception("error in listener")
                        if isinstance(e, MaxRetryError):
                            return

            # if not self.when_install:
            #     try:
            #         condition_element1 = self.driver.find_element_by_xpath("//android.widget.TextView[@text='了解详情']")
            #         condition_element2 = self.driver.find_element_by_xpath("//android.widget.TextView[@text='立即领取']")
            #         condition_element3 = self.driver.find_element_by_xpath("//android.widget.TextView[@text='立即抢购']")
            #         if condition_element1 or condition_element2 or condition_element3:
            #             element = self.driver.find_element_by_xpath("//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageView")
            #             if element:
            #                 element.click()
            #     except Exception, e:
            #         if isinstance(e, NoSuchElementException):
            #             pass
            #         else:
            #             LOGGING.exception("error in listener")
            #             if isinstance(e, MaxRetryError):
            #                 return

            time.sleep(1)
        LOGGING.info("listener stopped")
        return


