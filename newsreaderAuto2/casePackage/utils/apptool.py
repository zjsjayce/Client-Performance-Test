#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import sys
import functools
import subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "..")))
import casePackage.utils.constants as constants

import Utils.logger as logger

LOGGING = logger.get_logger(__name__)
NETEASE = 'netease'
SEARCHBOX = 'searchbox'
TOUTIAO = 'toutiao'
UC = 'uc'
QQ = 'qq'
TENCENT = 'tencent'
BAIDU = 'baidu'
CHROME = 'chrome'
QUARK = 'quark'
NETDISK = 'netdisk'
WEIXIN = 'wechat'
QIHOO = '360'
TIEBA = 'tieba'
NEWS = 'news'

# ANDROID_HOME = '/home/jenkins/Software/android-sdk-linux/'

huwei_device = ['DLQ0216408002491', 'SJE5T17429000361', 'SJE5T17623002873', 'MKJNW17C22011580', 'XPU4C17112010268', 'SJE0217C28004070', 'EJL4C17317001631']

bclass = constants.bclass

package = constants.package


# class sleep(object):
#     def __init__(self, func):
#         self._func = func
#         self.t = 2
#
#     def __call__(self, *args, **kwargs):
#         self._func()
#         time.sleep(self.t)

def adb_path():
    import platform
    sysstr = platform.system()
    if sysstr == "Windows":
        return 'adb '
    elif sysstr == "Linux":
        lines = os.popen("env").readlines()
        for line in lines:
            if 'ANDROID_HOME' in line:
                return os.path.join(line.split('=')[1].strip(), 'platform-tools/adb ')
    else:
        'adb '

def sleep(t=0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            func(*args, **kw)
            time.sleep(t)
        return wrapper
    return decorator

class apptool(object):
    def __init__(self, app, device, scene=None, android_home=None):
        self.app = app
        self.device = device
        self.scene = scene
        self.android_home = android_home or adb_path()
        if self.android_home:
            self.ADB_PATH = self.android_home
        else:
            self.ADB_PATH = 'adb'

    @sleep()
    def pmClearApp(self):
        LOGGING.debug("pm clear app " + self.app)
        cmd = self.ADB_PATH + "-s " + self.device + " shell pm clear " + package.get(self.app)
        os.system(cmd)
        LOGGING.debug("Executing adb cmd: " + cmd)

    @sleep()
    def forceStopApp(self):
        LOGGING.debug("force stop app " + self.app)
        cmd = self.ADB_PATH + "-s " + self.device + " shell am force-stop " + package.get(self.app)
        os.system(cmd)
        LOGGING.debug("Executing adb cmd: " + cmd)

    @sleep()
    def inputText(self, text):
        LOGGING.debug("input text " + text)
        cmd = self.ADB_PATH + "-s " + self.device + " shell input text " + text
        os.system(cmd)
        LOGGING.debug("Executing adb cmd: " + cmd)

    @sleep()
    def swith_input(self, method):
        input_method = None
        lines = os.popen(self.ADB_PATH + "-s " + self.device + " shell ime list -s").readlines()
        for line in lines:
            if method in line:
                input_method = line.strip()
                break
        if input_method:
             return os.system(self.ADB_PATH + "-s " + self.device + " shell ime set " + input_method)
        else:
            return False

    @sleep()
    def input_text(self, text, el=None, point=None):
        if len(text.split()) > 1:
            for i in range(0, len(text.split())):
                self.input_text(text.split()[i], el=el, point=point)
                subprocess.Popen(self.ADB_PATH + '-s ' + self.device + ' shell input keyevent 62', shell=True)
            # os.system(self.ADB_PATH + '-s ' + self.device + ' shell input keyevent 67')
            return
        if self.swith_input('adbkeyboard') == 0:
            return self.inputText(text)
        if el:
            el.click()
        if point:
            self.click_at(point[0], point[1])
        # cmd = self.ADB_PATH + '-s ' + self.device + ' shell am broadcast -a ADB_INPUT_TEXT --es msg "' + text.decode('utf8').encode('gbk') + 'a"'
        cmd = self.ADB_PATH + '-s ' + self.device + ' shell am broadcast -a ADB_INPUT_TEXT --es msg "' + text + '"'
        subprocess.Popen(cmd, shell=True)
        # time.sleep(2)
        # os.system(self.ADB_PATH + '-s ' + self.device + ' shell input keyevent 67')
        self.swith_input('sogou')

    @sleep()
    def enter(self):
        os.system(self.ADB_PATH + "-s " + self.device + " shell input keyevent 66")

    @sleep()
    def swipe(self, x, y, z, a):
        w, h = self.window_size()
        cmd = self.ADB_PATH + "-s " + self.device + " shell input swipe " + str(x * w) + " " + str(
            y * h) + " " + str(z * w) + " " + str(a * h) + " " + "900"
        LOGGING.debug("swipe from (" + str(x * w) + ", " + str(y * h) + ") to (" +  str(z * w) + ", " + str(a * h) + ")")
        os.system(cmd)
        LOGGING.debug("Executing adb cmd: " + cmd)

    def back(self):
        os.system(self.ADB_PATH + "-s " + self.device + " shell input keyevent 4")

    @sleep()
    def startApp(self):
        os.system(self.ADB_PATH + "-s " + self.device + " shell am start -n " + package.get(self.app) + "/" + bclass.get(self.app))

    def start(self):
        os.system(self.ADB_PATH + "-s " + self.device + " shell am start -n " + package.get(self.app) + "/" + bclass.get(self.app))

    @sleep()
    def home(self):
        os.system(self.ADB_PATH + '-s ' + self.device + ' shell input keyevent 3')

    def _activityBack(self):
        lines = os.popen(self.ADB_PATH + "-s " + self.device + " shell dumpsys activity | grep mFocusedActivity").readlines()
        for line in lines:
            if package.get(self.app) in line:
                return True
        return False

    @sleep()
    def stop_app_back(self):
        while self._activityBack():
            self.back()

    @sleep()
    def click_at(self, x, y):
        click_cmd = self.ADB_PATH + "-s " + self.device + " shell input tap " + str(x) + " " + str(y)
        os.system(click_cmd)

    def get_brand(self):
        cmd = self.ADB_PATH + "-s " + self.device + " shell getprop ro.product.brand"
        LOGGING.debug("Executing adb cmd: " + cmd)
        brand = os.popen(cmd)
        return brand.read().strip('\r\n')

    def get_android_version(self):
        cmd = self.ADB_PATH + "-s " + self.device + " shell getprop ro.build.version.release"
        print(cmd)
        android_version = os.popen(cmd)
        return android_version.read().strip('\r\n')

    def get_model(self):
        cmd = self.ADB_PATH + "-s " + self.device + " shell getprop ro.product.model"
        LOGGING.debug("Executing adb cmd: " + cmd)
        model = os.popen(cmd)
        return model.read().strip('\r\n')

    def __get_rom(self):
        brand = self.get_brand()
        if brand == 'HUAWEI' or brand == 'HONOR':
            cmd = self.ADB_PATH + "-s " + self.device + " shell getprop ro.build.version.emui"
            LOGGING.debug("Executing adb cmd: " + cmd)
            rom = os.popen(cmd)
        return rom.read().strip('\r\n')

    def get_rom_name(self):
        brand = self.get_brand()
        if brand == 'HUAWEI' or brand == 'HONOR':
            romName = self.__get_rom().split("_")[0]
        if brand == 'Xiaomi':
            cmd = self.ADB_PATH + "-s " + self.device + " shell getprop ro.miui.ui.version.name"
            LOGGING.debug("Executing adb cmd: " + cmd)
            romName = os.popen(cmd).read().strip('\r\n')
        return romName

    def get_rom_version(self):
        brand = self.get_brand()
        if brand == 'HUAWEI' or brand == 'HONOR':
            romVersion = self.__get_rom().split("_")[1]
        if brand == 'Xiaomi':
            cmd = self.ADB_PATH + "-s " + self.device + " shell getprop ro.miui.ui.version.code"
            LOGGING.debug("Executing adb cmd: " + cmd)
            romVersion = os.popen(cmd).read().strip('\r\n')
        return romVersion

    def get_app_version(self):
        cmd = self.ADB_PATH + "-s " + self.device + " shell dumpsys package " + package.get(self.app) + "|grep versionName"
        print cmd
        result = os.popen(cmd)
        version = result.read().strip('\r\n').split("=")[1]
        return version

    @sleep()
    def loadURL(self, url):
        os.system(self.ADB_PATH + "-s " + self.device + " shell am start -n " + package.get(self.app) + "/" + bclass.get(self.app)
                + " -a android.intent.action.VIEW -d " + url)

    def getFlowBefore(self):
        print package.get(self.app) + "_flow_" + self.scene + "_0"
        sys.stdout.flush()
        time.sleep(5)

    def getFlowAfter(self):
        print package.get(self.app) + "_flow_" + self.scene + "_1"
        sys.stdout.flush()
        time.sleep(2)

    def getCPU(self):
        print package.get(self.app) + "_cpu_" + self.scene
        sys.stdout.flush()

    def getMEM(self):
        print package.get(self.app) + "_memery_" + self.scene
        sys.stdout.flush()
        time.sleep(5)

    def getFramesStart(self):
        print package.get(self.app) + "_frames_" + self.scene + "_0"
        sys.stdout.flush()
        time.sleep(5)

    def getFramesEnd(self):
        print package.get(self.app) + "_frames_" + self.scene + "_1"
        sys.stdout.flush()
        time.sleep(5)

    def getDataStart(self, sc):
        print package.get(self.app) + "__getPerformanceData__actionStart__" + sc
        sys.stdout.flush()
        time.sleep(5)

    def getDataEnd(self, sc, lop):
        for i in range(0, 5):
            print package.get(self.app) + "__getPerformanceData__actionEnd__" + sc + "__" + str(lop)
            sys.stdout.flush()
            time.sleep(2)

    def window_size(self):
        # 通用方式
        sp = 'init='
        lines = os.popen(
            self.ADB_PATH + "-s " + self.device + " shell dumpsys window displays |head -n 3 | grep init").readlines()
        for line in lines:
            if sp in line:
                list = line.strip().split()
                for l in list:
                    if 'init' in l:
                        w = int(l.split(sp)[1].split('x')[0].strip())
                        h = int(l.split(sp)[1].split('x')[1].strip())
                        return w, h
        # 高通方式
        sp = 'Physical size:'
        lines = os.popen(self.ADB_PATH + "-s " + self.device + " shell wm size").readlines()
        for line in lines:
            if sp in line:
                list = line.strip().split()
                for l in list:
                    if 'x' in l:
                        w = int(l.split('x')[0].strip())
                        h = int(l.split('x')[1].strip())
                        return w, h

    # @sleep(1)
    # def getVideo(self):
    #     if self.device in huwei_device:
    #         os.system(self.ADB_PATH + '-s ' +self.device + ' shell rm /storage/emulated/0/Pictures/Screenshots/*.mp4')
    #         self.swipe(0.5, 0.01, 0.5, 0.8)
    #         time.sleep(1)
    #         self.swipe(0.5, 0.3, 0.5, 0.8)
    #         import tools
    #         x, y = tools.find_text('屏幕录制', self.device)
    #         try:
    #             self.click_at(x, y)
    #             time.sleep(3)
    #             print 'start'
    #         except:
    #             raise Exception('get video error!')
    #     else:
    #         w, h = self.window_size()
    #         subprocess.Popen(self.ADB_PATH + "-s " + self.device +
    #                      " shell screenrecord --size " + str(w) + "x" + str(h) + " --time-limit 10 /sdcard/screenrecord.mp4",
    #                      stdout=subprocess.PIPE,
    #                      shell=True)

    # def saveVideo(self):
    #     videoName = "video"
    #     tmp_save = os.path.join(os.path.join(constants.AUTO_PATH, self.device), self.scene)
    #     if not os.path.exists(tmp_save):
    #         os.makedirs(tmp_save)
    #
    #     cur_path = os.getcwd()
    #     os.chdir(tmp_save)
    #
    #     if self.device in huwei_device:
    #         self.click_at(100, 30)
    #         LOGGING.debug()'close'
    #         time.sleep(1)
    #         lines = os.popen(
    #             self.ADB_PATH + "-s " + self.device + " shell ls /storage/emulated/0/Pictures/Screenshots/*.mp4").readlines()
    #         print self.ADB_PATH + "-s " + self.device + " shell ls /storage/emulated/0/Pictures/Screenshots/*.mp4"
    #         for line in lines:
    #             if '.mp4' in line:
    #                 file_name = line.strip().split('/')[-1]
    #                 os.system(
    #                     self.ADB_PATH + "-s " + self.device + " pull /storage/emulated/0/Pictures/Screenshots/" +
    #                     file_name + " " + tmp_save + "/" + videoName + ".mp4")
    #                 print self.ADB_PATH + "-s " + self.device + " pull /storage/emulated/0/Pictures/Screenshots/" + \
    #                       file_name + " " + tmp_save + "/" + videoName + ".mp4"
    #                 break
    #     else:
    #         os.system(self.ADB_PATH + "-s " + self.device + " pull /sdcard/screenrecord.mp4 "
    #                   + tmp_save + "/" + videoName + ".mp4")
    #     ffmpeg_cmd = 'ffmpeg -i ' + videoName + '.mp4 -r 30 -f image2 image-%3d.jpg'
    #     # video_length = "ffmpeg -i demo.mp4 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
    #     os.system(ffmpeg_cmd)
    #     os.chdir(cur_path)
    #     video_abs_path = tmp_save + videoName + '.mp4'
    #     if not os.path.exists(video_abs_path):
    #         LOGGING.error('video generate failed. video file does not exist.')
    #     return tmp_save

    def net(self):
        lines = os.popen(
            self.ADB_PATH + "-s " + self.device + " shell ifconfig").readlines()
        wlan = False
        for line in lines:
            if line.find('wlan0') > -1:
                wlan = True
                continue
            if wlan and line.strip() == '':
                return '4G'
            if wlan and line.find('inet addr') > -1:
                return 'wifi'
        return '4G'


if __name__ == "__main__":
    app = apptool('toutiao', 'XPU4C17112010268')
    print app.get_rom_name()
    print app.get_rom_version()




