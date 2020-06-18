# -*- coding: utf-8 -*-
import functools
import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# sys.path.append(os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "..")))
import time

import requests

from Utils.logger import get_logger
import casePackage.otherThread.env as env
from casePackage.utils import constants

LOGGING = get_logger(__name__)
ADB_PATH = 'adb'

def sleep(t=0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            func(*args, **kw)
            time.sleep(t)
        return wrapper
    return decorator

def get_app_version(device, package_name):
    cmd = ADB_PATH + " -s " + device + " shell dumpsys package " + package_name + "|findstr versionName"
    LOGGING.debug("Excuting adb cmd: " + cmd)
    result = os.popen(cmd).read().strip('\r\n')
    print result
    if not result:
        print 'app is not existed'
        return 'not existed'
    version = result.split("=")[1]
    return version

def install_app(device, apk_location):
    cmd = ADB_PATH + " -s " + device + " install " + apk_location
    LOGGING.debug("Start to install app: " + cmd)
    result = os.popen(cmd).read().strip('\r\n')
    LOGGING.info(result)
    if result.lower().__contains__('success'):
        return True
    else:
        return False

def uninstall_app(device, package_name):
    cmd = ADB_PATH + " -s " + device + " shell pm uninstall " + package_name
    LOGGING.debug("Excuting adb cmd: " + cmd)
    result = os.popen(cmd).read().strip('\r\n')
    print result
    if result.__contains__('success'):
        return True
    else:
        return False

def downloadApp(apk_url, branchName):
    LOGGING.info("download apk via url: " + apk_url)
    r = requests.get(apk_url)  # create HTTP response object
    LOGGING.info("download finished: " + apk_url)
    apk_path = os.path.join(os.path.join(os.getcwd(), "res"), "apk")
    apk_name = branchName + ".apk"
    with open(os.path.join(apk_path, apk_name), 'wb') as f:
        f.write(r.content)
    return str(os.path.join(apk_path, apk_name))

def check_installed_version(device, force_install, app, app_version, apk_location, apk_url, branchName, suite):
    package_name = constants.package.get(app)
    # 如果有url参数，下载指定apk并存在../res/apk目录中
    if suite == "netease_grey_biz" and force_install and apk_url and branchName:
        apk_new_location = downloadApp(apk_url, branchName.replace("/", "_"))
        updateApp(apk_new_location, device, package_name)
        return get_app_version(device, package_name)
    # 如果没有url参数，则强制重新安装apk_loaction对应的apk
    if force_install:
        updateApp(apk_location, device, package_name)
        return get_app_version(device, package_name)
    installed_version = get_app_version(device, package_name)

    # version not the same, then update, no matter upgrade or downgrade
    if app_version == installed_version:
        return get_app_version(device, package_name)
    else:
        updateApp(apk_location, device, package_name)
        return get_app_version(device, package_name)


def updateApp(apk_location, device, package_name):
    install_listener, install_driver = env.getDriver('myapplication2', 'config.ini', device, True)
    LOGGING.debug("Start to uninstall app in updateApp: " + package_name)
    uninstall_app(device, package_name)
    time.sleep(5)
    LOGGING.debug("Start to install app in updateApp: " + apk_location)
    install_result = install_app(device, apk_location)
    install_listener.stop()
    LOGGING.info("Install listener stopped.")
    install_driver.quit()
    LOGGING.info("Install session closed.")
    if not install_result:
        raise Exception("update app failed due to install failed.")

def startEmmageeService(device, monitored_app, csvFileName, monitor_interval = 1):
    cmd = "adb -s " + device + " shell am broadcast -a com.example.zhaoyuting.emmageespecial.broadcast.StartMonitorReceiver --es packageName " \
          + monitored_app + " --es csvFile " + constants.emmagee_dir + csvFileName + " --ei interval " + str(monitor_interval) + " --include-stopped-packages"
    LOGGING.debug("Excuting adb cmd: "  + cmd)
    result = os.popen(cmd).read().strip('\r\n')
    LOGGING.debug(result)

def stopEmmageeService(device):
    cmd = "adb -s " + device + " shell am broadcast -a com.example.zhaoyuting.emmageespecial.broadcast.StopMonitorReceiver"
    LOGGING.debug("Excuting adb cmd: " + cmd)
    result = os.popen(cmd).read().strip('\r\n')
    LOGGING.debug(result)

def pullFile(device, sourcePath, destPath):
    cmd = "adb -s " + device + " pull " + sourcePath + " " + destPath
    LOGGING.debug("Excuting adb cmd: " + cmd)
    result = os.popen(cmd).read().strip('\r\n')
    LOGGING.debug(result)

def press_back(device):
    LOGGING.debug("Press back")
    input_keyevent(device, constants.KEYCODE_BACk)

def press_back_twice(device):
    LOGGING.debug("Press back twice")
    input_keyevent(device, constants.KEYCODE_BACk)
    input_keyevent(device, constants.KEYCODE_BACk)

def input_keyevent(device, event_code):
    cmd = "adb -s " + device + " shell input keyevent " + str(event_code)
    LOGGING.debug("Excuting adb cmd: " + cmd)
    result = os.popen(cmd).read().strip('\r\n')
    LOGGING.debug(result)

# @sleep()
def pmClearApp(device, app):
    LOGGING.debug("pm clear app " + app)
    cmd = ADB_PATH + " -s " + device + " shell pm clear " + constants.package.get(app)
    os.system(cmd)
    LOGGING.debug("Executing adb cmd: " + cmd)

# @sleep()
def forceStopApp(device, app):
    LOGGING.debug("force stop app " + app)
    cmd = ADB_PATH + " -s " + device + " shell am force-stop " + constants.package.get(app)
    os.system(cmd)
    LOGGING.debug("Executing adb cmd: " + cmd)

# @sleep()
def startApp(device, app):
    LOGGING.debug("start app " + app)
    cmd = ADB_PATH + " -s " + device + " shell am start -n " + constants.package.get(app) + "/" + constants.bclass.get(app)
    os.system(cmd)
    LOGGING.debug("Executing adb cmd: " + cmd)

def prepareEmmageeService(device):
    cmd = "adb -s " + device + " shell am start -n com.example.zhaoyuting.emmageespecial/.activity.MainPageActivity"
    LOGGING.debug("Excuting adb cmd: " + cmd)
    result = os.popen(cmd).read().strip('\r\n')
    LOGGING.debug(result)
    input_keyevent(device, constants.KEYCODE_HOME)

def killTaskByName(taskName):
    findPIDCmd = "tasklist|findstr " + taskName
    LOGGING.debug("Executing tasklist cmd: " + findPIDCmd)
    result = os.popen(findPIDCmd).read().strip('\r\n').split('\n')
    for line in result:
        pid = line
    LOGGING.debug(result)
    return result


def adb_kill_server():
    cmd = "adb kill-server"
    LOGGING.debug("Excuting adb cmd: " + cmd)
    os.popen(cmd).read().strip('\r\n')

def adb_devices():
    cmd = "adb devices"
    LOGGING.debug("Excuting adb cmd: " + cmd)
    result = os.popen(cmd).read().strip('\r\n')
    LOGGING.debug(result)


def adb_forcestop_appiumio(device):
    cmd = "adb -s " + device + " shell am force-stop io.appium.uiautomator2.server"
    LOGGING.debug("Excuting adb cmd: " + cmd)
    result = os.popen(cmd).read().strip('\r\n')


def restart_adb(device):
    adb_kill_server()
    adb_devices()
    adb_forcestop_appiumio(device)


if __name__ == '__main__':
    print downloadApp("http://teamcity.ws.netease.com/guestAuth/repository/download/bt6/.lastSuccessful/newsreader-nightly.apk", "111")