# # -*- coding: utf-8 -*-
#
# import threading
# from appium import webdriver
# import os
# import sys
# from casePackage.utils import apptool
# from ConfigParser import ConfigParser
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#
# def getConfig(file='config.ini'):
#     cf = ConfigParser()
#     file_path = os.path.join(os.path.join(os.path.abspath('..'), 'config'), file)
#     if not os.path.exists(file_path):
#         file_path = os.path.join(os.path.join(os.getcwd(), 'casePackage/config'), file)
#     if not os.path.exists(file_path):
#         file_path = os.path.join('home/jenkins/Source/LRP/lrp/casePackage/config', file)
#     cf.read(file_path)
#     return cf
#
#
# def getDriver(app, file='config.ini', device=None, installing=False):
#     cf = getConfig(file)
#     desired_caps = {}
#     desired_caps["platformName"] = cf.get("init", "platformName")
#     if device:
#         desired_caps["platformVersion"] = cf.get(device, 'platformVersion')
#         desired_caps["deviceName"] = cf.get(device, 'deviceName')
#     else:
#         desired_caps["platformVersion"] = cf.get('init', 'platformVersion')
#         desired_caps["deviceName"] = cf.get('init', 'deviceName')
#     desired_caps['noReset'] = True
#     desired_caps["unicodeKeyboard"] = False
#     desired_caps["resetKeyBoard"] = False
#     desired_caps["appPackage"] = cf.get(app, 'appPackage')
#     desired_caps["appActivity"] = cf.get(app, 'appActivity')
#     try:
#         desired_caps["appWaitActivity"] = cf.get(app, 'appWaitActivity')
#     except:
#         pass
#
#     print 'start'
#     desired_caps["newCommandTimeout"] = 600
#     # desired_caps["commandTimeouts"] = 20
#     # desired_caps["automationName"] = "UiAutomator2"
#     driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
#     driver.implicitly_wait(2)
#     if app == apptool.TOUTIAO:
#         l = listener(desired_caps["deviceName"], app, '始终允许/同意', driver)
#         l.start()
#     else:
#         l = listener(desired_caps["deviceName"], app, '始终允许/允许', driver)
#         l.start()
#     if installing:
#         l = listener(desired_caps["deviceName"], app, '立即删除/继续安装', driver)
#         l.start()
#     # import xmltodict
#     # import json
#     # print json.dumps(xmltodict.parse(driver.page_source))
#     # import time
#     # time.sleep(20)
#     # print driver.find_element_by_xpath("//android.widget.TextView[@text='百度']").location
#     # print driver.find_element_by_xpath("//android.widget.TextView[@text='百度']").size
#     # print driver.find_element_by_xpath("//android.widget.TextView[@text='首页']").id
#     return l, driver
#
# class listener(threading.Thread):
#     def __init__(self, device, app, text, driver, is_stopped = False):
#         threading.Thread.__init__(self)
#         self.device = device
#         self.app = app
#         self.text = str(text).split("/")
#         self.driver = driver
#         self.is_stopped = is_stopped
#
#     def stop(self):
#         self.is_stopped = True
#
#     def run(self):
#         apptools = apptool.apptool(self.app, self.device, ' ')
#         apptools.startApp()
#         while not self.is_stopped:
#             for k in self.text:
#                 xpath_id = "//android.widget.Button[contains(@text, '" + k + "')]"
#                 # print xpath_id
#                 try:
#                     element = self.driver.find_element_by_xpath(xpath_id)
#                     if element:
#                         element.click()
#                 except:
#                     pass
#         return