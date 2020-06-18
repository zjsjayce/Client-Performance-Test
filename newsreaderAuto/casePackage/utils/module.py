#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import subprocess

import apptool
import time

import Utils.logger as logger
import constants
import tools
import threading

# def set_timeout(num):
#     import signal
#     def wrap(func):
#         def handle(signum, frame):
#             raise Exception("no element")
#
#         def to_do(*args, **kwargs):
#             try:
#                 signal.signal(signal.SIGALRM, handle)
#                 signal.alarm(num)
#                 r = func(*args, **kwargs)
#                 signal.alarm(0)
#                 return r
#             except Exception as e:
#                 return None
#
#         return to_do
#     return wrap

# LOGGING = logger.Logger().get_logger(__name__)
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from urllib3.exceptions import MaxRetryError

LOGGING = logger.get_logger(__name__)


def _async_raise(tid, exctype):
    import inspect
    import ctypes
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class Get_element_by_thread(threading.Thread):
    def __init__(self, driver, path):
        threading.Thread.__init__(self)
        self.driver = driver
        self.path = path
        self.element = None

    def run(self):
        try:
            if "//" in self.path:
                self.element = self.driver.find_element_by_xpath(self.path)
            else:
                self.element = self.driver.find_element_by_id(self.path)
        except Exception as e:
            pass


class module(object):
    def __init__(self, driver, app, apptools, batch_num):
        self.driver = driver
        self.app = app
        self.apptools = apptools
        self.batch_num = batch_num

    def mi4(self):
        if self.apptools.device == '532ff62c' and (self.app == apptool.SEARCHBOX or self.app == apptool.TOUTIAO):
            print 'start init'
            self.app_start_init()
            time.sleep(30)
            print 'check login'
            self.check_login_alert()
            return True
        return False

    def restart_app(self, device=None):
        if self.mi4():
            return
        self.apptools.forceStopApp()
        self.apptools.startApp()
        self.app_permission()
        if self.app == apptool.SEARCHBOX:
            time.sleep(5)
            self.check_update_alert()
            self.apptools.back()
            self.check_login_alert()
        if self.app == apptool.TOUTIAO:
            self.check_update_alert()
        if self.app == apptool.UC:
            self.first_start_alert()
            self.app_permission()
        if self.app == apptool.QQ:
            self.clilc_by_text("知道了", device)
            self.app_permission()
            self.clilc_by_text("跳过", device)
            self.app_permission()
            self.clilc_by_text("知道了", device)
            self.app_permission()
        if self.app == apptool.CHROME:
            self.clilc_by_text("接受并继续", device)
            e = self.find_element("//android.widget.Button[@text='更新']")
            if e:
                e.click()
            self.clilc_by_text("谢谢", device)
            time.sleep(2)
            self.clilc_by_text("继续使用", device)
        if self.app == apptool.NEWS:
            pass

        if self.app == apptool.QUARK:
            # self.app_permission()
            self.check_update_alert()
        if self.app == apptool.NETDISK:
            try:
                self.find_element("com.baidu.netdisk:id/close_btn").click()
            except:
                pass
        if self.app == apptool.QIHOO:
            self.clilc_by_text("点击进入", device)
            self.clilc_by_text("同意并继续", device)
            time.sleep(10)
            self.app_permission(3)

    def first_start_alert(self):
        if self.app == apptool.UC:
            for i in range(0, 3):
                try:
                    self.find_element("//android.widget.TextView[@text='同意并继续']").click()
                except:
                    pass

    def find_app_icon_from_desktop(self):
        self.apptools.home()
        if self.app == apptool.SEARCHBOX:
            text = '百度'
        if self.app == apptool.TOUTIAO:
            text = '今日头条'
        if self.app == apptool.TIEBA:
            text = '百度贴吧'
        if self.app == apptool.NEWS:
            text = '百度新闻'
        for i in range(0, 10):
            element = self.find_element("//android.widget.TextView[@text='" + text + "']") or \
                      self.find_element("//android.widget.TextView[@text='@" + text + "']")
            if element:
                return element
            self.apptools.swipe(0.8, 0.5, 0.1, 0.5)
        return None

    def v_10_8(self, device=None):
        self.apptools.swipe(0.8, 0.5, 0.2, 0.5)
        self.clilc_by_text('立即开启', device)

    def app_start_init(self, device=None):
        try:
            self.find_app_icon_from_desktop().click()
            # self.v_10_8(device)
        except:
            print "no app icon found."
        click = False
        for i in range(0, 10):
            try:
                self.find_element("com.baidu.searchbox:id/introduction_entrance").click()
                continue
            except:
                pass
            try:
                element = self.find_element("//android.widget.TextView[@text='同意并继续']") or \
                          self.find_element("//android.widget.Button[@text='同意并继续']")
                element.click()
                click = True
            except:
                if click:
                    break
        time.sleep(5)
        self.app_permission()
        self.check_update_alert()
        self.check_login_alert()

    def swith_to_night(self):
        self.app_start_init()
        self.restart_app()
        if self.app == apptool.TOUTIAO:
            try:
                element = self.find_element(
                    "//android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ImageView") \
                          or self.find_element("//android.widget.TextView[@text='未登录']")
                element.click()
                time.sleep(1)
                self.find_element(
                    "//android.widget.LinearLayout/android.widget.LinearLayout/android.view.View[@index=2]").click()
                time.sleep(2)
                return True
            except:
                return False
        try:
            el = self.find_element("//android.widget.TabWidget/android.widget.FrameLayout[@index=4]")
            el.click()
            time.sleep(1)
            self.find_element("//android.widget.TextView[@text='夜间模式']").click()
            time.sleep(2)
            return True
        except:
            return False

    def app_permission(self, count=None):
        for i in range(0, count or 5):
            try:
                self.find_element("//android.widget.Button[@text='始终允许']").click()
            except:
                time.sleep(1)
                pass

    def app_start_init_toutiao(self):
        try:
            self.find_app_icon_from_desktop().click()
        except:
            print "no app icon found."
            self.apptools.startApp()
        time.sleep(10)

    def check_update_alert(self):
        if self.app == apptool.QUARK:
            for i in range(0, 3):
                try:
                    self.find_element("//android.widget.Button[@text='取消']").click()
                    return
                except:
                    time.sleep(1)
                    pass
        if self.app == apptool.TOUTIAO:
            for i in range(0, 3):
                try:
                    self.find_element("//android.widget.TextView[@text='以后再说']").click()
                    return
                except:
                    time.sleep(1)
                    pass
        else:
            for i in range(0, 3):
                try:
                    element = self.find_element("com.baidu.searchbox:id/update_close") or \
                              self.find_element("com.baidu.searchbox:id/close")
                    element.click()
                    time.sleep(1)
                    return
                except:
                    pass

    def check_login_alert(self):
        time.sleep(5)
        # for i in range(0, 3):
        #     try:
        #         element = self.find_element("com.baidu.searchbox:id/close_btn") \
        #                   or self.find_element("com.baidu.searchbox:id/half_screen_mask_close")
        #         element.click()
        #         return
        #     except:
        #         pass
        self.apptools.back()
        time.sleep(4)
        self.apptools.back()
        time.sleep(4)
        return

    def clilc_by_text(self, text, device):
        try:
            x, y = tools.find_text_with_pos(text, device)
            if not x:
                return
            self.apptools.click_at(x, y)
        except:
            pass

    # def find_tuwen(self, device):
    #     if self.app == apptool.SEARCHBOX:
    #         for i in range(1, 5):
    #             element = self.find_element(
    #                 "//android.widget.RelativeLayout[@index=" + str(i) + "]/android.widget.ImageView[@index=3]")
    #             if element:
    #                 element_b = self.find_element(
    #                     "//android.widget.RelativeLayout[@index=" + str(i) + "]/android.widget.TextView[@index=4]")
    #                 if not element_b:
    #                     x, y = tools.find_text("广告", device)
    #                     if y:
    #                         element_p = self.driver.find_element_by_xpath(
    #                             "//android.widget.RelativeLayout[@index=" + str(i) + "]")
    #                         if y > element_p.location.get('y') and y < element_p.location.get('y') + element_p.size.get(
    #                                 'height'):
    #                             print element_p.location.get('y') + element_p.size.get('height')
    #                             continue
    #                     else:
    #                         return element
    #
    #     if self.app == apptool.TOUTIAO:
    #         if self.apptools.net() == '4G':
    #             for i in range(1, 10):
    #                 element = self.find_element("//android.widget.LinearLayout[@index=" + str(i) +
    #                                             "]/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.ImageView")
    #                 if element:
    #                     element_b = self.find_element("//android.widget.LinearLayout[@index=" + str(i) +
    #                                                   "]/android.widget.RelativeLayout/android.widget.FrameLayout/android.view.View")
    #                     if not element_b:
    #                         return element
    #                 else:
    #                     return None
    #         element = self.find_element(
    #             "//android.widget.LinearLayout/android.support.v7.widget.LinearLayoutCompat/android.widget.ImageView[@index=2]")
    #         x, y = tools.find_text("广告", device)
    #         if element and not x:
    #             return element

    def find_tuji(self):
        # list = []
        # for i in range(3, 20):
        #     list.append(str(i) + "图")
        # for text in list:
        #     element = self.find_element("//android.widget.TextView[@text='" + text + "']")
        #     if element:
        #         return element
        element = self.find_element("//android.widget.LinearLayout/android.view.ViewGroup/android.widget.ImageView[@index=0]")
        if element:
            return element
        return False

    def tencent_find_tuji_item(self):
        element = self.find_element("com.tencent.news:id/title_text")
        if element:
            return element

    def netease_find_tuwen_item(self):
        # 返回第三条图文
        for retryCount in range(1, 4):
            element = self.find_element("//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[@index=1]")
            if element:
                break
            else:
                time.sleep(0.5)
                LOGGING.warn("Didn't find tuwen item after %d times trial" % retryCount)
        return element

    def netease_find_tuwen_item_in_basic(self):
        element = self.find_element("//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[@index=1]")
        try:
            if element:
                ad_element = self.find_element(
                    "//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[@index=1]/\
                    android.widget.RelativeLayout[@index=0]/android.widget.RelativeLayout[@index=2]/android.widget.TextView[@text='广告']")
                if ad_element:
                    LOGGING.info("Find Ad in netease_find_tuwen_item_in_basic, return empty string")
                    return ""

                video_element = self.find_element("//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView[@index=2]")
                if video_element:
                    LOGGING.info("Find Video in netease_find_tuwen_item_in_basic, return empty string")
                    return ""

                textView_element = self.find_element(
                    "//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[@index=1]/android.widget.LinearLayout[@index=0]/android.widget.TextView")
                return textView_element
            else:
                return ""
        except Exception, e:
            LOGGING.exception("error occurs in netease_find_tuwen_item_in_basic", e)

    def toutiao_find_tuwen_item(self):
        # 返回第二条图文, 今日头条推荐页新闻index从3开始记，所以第二条index=5
        element = self.find_element("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[@index=4]")
        return element

    def tencent_find_tuwen_item(self):
        # 返回第二条图文, 今日头条推荐页新闻index从3开始记，所以第二条index=5
        element = self.find_element("com.tencent.news:id/title_text")
        return element

    def netease_find_tuji_item(self):
        list = []
        for i in range(3, 20):
            list.append(str(i) + "pics")
        for retryCount in range(1, 4):
            for text in list:
                element = self.find_element("//android.widget.TextView[@text='" + text + "']")
                if element:
                    return element
            if not element:
                LOGGING.warn("Didn't find tuwen item after %d times trial" % retryCount)
                time.sleep(0.5)
        return None

    def netease_find_tuji_tab(self):
        element = self.find_element("//android.widget.RelativeLayout/android.widget.TextView[@text='图片']")
        if element:
            return element
        return False

    def toutiao_find_tuji_tab(self):
        element = self.find_element("//android.widget.LinearLayout/android.view.View[@content-desc='图片']")
        if element:
            return element
        return False

    def switch_to_video_pindao(self):
        if self.app == apptool.TOUTIAO:
            self.find_element("//android.widget.TextView[@text='西瓜视频']").click()
        if self.app == apptool.SEARCHBOX:
            self.find_element("//android.widget.TextView[@text='好看视频']").click()

    def video_init(self, device=None):
        if self.apptools.net() == "4G":
            self.restart_app()
            self.switch_to_video_pindao()
            time.sleep(5)
            self.find_video_from_list(device).click()
            time.sleep(5)
            if self.app == apptool.TOUTIAO:
                element = self.find_element("//android.widget.TextView[@text='继续播放']")
                if element:
                    element.click()
            if self.app == apptool.SEARCHBOX:
                self.clilc_by_text('继续播放', device)
                time.sleep(2)
                self.find_element("//android.widget.TextView[@text='百度']").click()
        else:
            self.restart_app()

    def netease_find_shipin_tab(self):
        element = self.find_element("//android.widget.RelativeLayout/android.widget.TextView[@text='视频']")
        if element:
            return element
        return None

    def toutiao_find_shipin_tab(self):
        element = self.find_element("//android.widget.LinearLayout/android.view.View[@content-desc='视频']")
        if element:
            return element
        return None

    def tencent_find_shipin_tab(self):
        element = self.find_element("//android.widget.LinearLayout/android.widget.TextView[@text='视频']")
        if element:
            return element
        return None

    def tencent_find_tuji_tab(self):
        element = self.find_element("//android.widget.LinearLayout/android.widget.TextView[@text='图片']")
        return element

    # 返回“赞”图标
    def netease_find_video_item(self):
        for retryCount in range(1, 4):
            element = self.find_element(
                "//android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.ImageView")
            if element:
                return element
            else:
                time.sleep(0.5)
                LOGGING.warn("Didn't find zan item after %d times trial" % retryCount)
        return None

    def netease_find_video_start(self):
        element = self.find_element(
            "//android.support.v7.widget.RecyclerView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView")
        if element:
            return element
        return None

    # 返回“评论”图标
    def toutiao_find_video_item(self):
        element = self.find_element(
            "//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout[@index=2]/android.widget.TextView")
        if element:
            return element
        return False

    def tencent_find_video_item(self):
        element = self.find_element(
            "com.tencent.news:id/tv_comment_num")
        if element:
            return element
        return False

    def toutiao_find_video_start(self):
        element = self.find_element(
            "//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[@index=3]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ImageView[@index=2]")
        if element:
            return element
        return False

    def tencent_find_video_start(self):
        element = self.find_element(
            "com.tencent.news:id/video_play_normal")
        if element:
            return element
        return False

    def find_video(self, device=None):
        if self.app == apptool.TOUTIAO:
            element = self.find_element("//android.widget.RelativeLayout/android.view.View[@index=1]")
            if element:
                return element
            return False
        x, y = tools.find_text_with_pos("小视频", device)
        if device and y and y < self.driver.get_window_size()['height'] * 0.9 and y > self.driver.get_window_size()[
            'height'] * 0.1:
            return False
        list = []
        for i in range(1, 5):
            for j in range(10, 59):
                list.append('0' + str(i) + ':' + str(j))
        for text in list:
            element = self.find_element("//android.widget.TextView[@text='" + text + "']")
            if element:
                for num in range(0, 5):
                    el = self.find_element("//android.widget.RelativeLayout[@index=" + str(num) +
                                           "]/android.widget.RelativeLayout/android.widget.TextView[@text='"
                                           + text + "']")
                    if el:
                        try:
                            el_b = self.driver.find_element_by_xpath(
                                "//android.widget.RelativeLayout[@index=" + str(num)
                                + "]/android.view.ViewGroup[@index=2]")
                        except:
                            continue
                        x, y = tools.find_text_with_pos("广告", device)
                        if y and el_b and y >= el_b.location.get('y') and y <= el_b.location.get('y') + el_b.size.get(
                                'height'):
                            print 'ad'
                            continue
                        else:
                            return element
                    else:
                        continue
        return False

    def find_video_from_list(self, device=None):
        if self.app == apptool.TOUTIAO:
            element = self.find_element("//android.widget.RelativeLayout/android.view.View[@index=4]")
            if element:
                return element
            return False
        if self.app == apptool.SEARCHBOX:
            el = self.find_element(
                "//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout/android.widget.TextView")
            if el:
                return el
            return self.find_video(device)

    def _get_element_by_text(self, text):
        try:
            element = self.driver.find_element_by_name(text) or self.driver.find_element_by_accessibility_id(text)
            if element:
                x, y = self.element_point(element)
                from element import element
                element = element(self.driver, x, y)
                return element
        except:
            return False

    # def find_element_immediately(self, xpath):
    #     import time
    #     cur_time = time.time()
    #     while time.time() - cur_time < 10:
    #         element = self.find_element(xpath)
    #         if element:
    #             return element
    #
    # # @set_timeout(2)
    # def find_element(self, id):
    #     try:
    #         f = Get_element_by_thread(self.driver, id)
    #         f.start()
    #         cur_time = time.time()
    #         while time.time() - cur_time < 2:
    #             element = f.element
    #             if f.element:
    #                 break
    #         if not f.element:
    #             _async_raise(f.ident, SystemExit)
    #         if element:
    #             x, y = self.element_point(element)
    #             from element import element
    #             element = element(self.driver, x, y)
    #             return element
    #     except Exception as e:
    #         # print e
    #         return None

    def find_element_immediately(self, xpath):
        import time
        cur_time = time.time()
        while time.time() - cur_time < 10:
            try:
                if '//' in xpath:
                    element = self.driver.find_element_by_xpath(xpath)
                else:
                    element = self.driver.find_element_by_id(xpath)
                if element:
                    return element
            except:
                continue

    # @set_timeout(2)
    def find_element(self, id):
        try:
            if '//' in id:
                original_element = self.driver.find_element_by_xpath(id)
            else:
                original_element = self.driver.find_element_by_id(id)
            if original_element:
                # x, y = self.element_point(original_element)
                from element import Element
                derived_element = Element(self.driver, original_element)
                return derived_element
        except Exception, e:
            if isinstance(e, NoSuchElementException):
                LOGGING.warn("Didn't find wanted element in find_element. Catch NoSuchElementException.")
                return None
            else :
                # In order to log all exception and don't miss any, didn't use "except MaxRetruError" or "except WebDriverException"
                LOGGING.exception("error in find_element")
                if isinstance(e, MaxRetryError) or isinstance(e, WebDriverException):
                    LOGGING.exception("Catch MaxRetryError or WebDriverException, need to quit driver and rerun the casePackage.")
                    raise

    def huawei_screen(self):
        self.apptools.swipe(0.5, 0.01, 0.5, 0.8)
        time.sleep(2)
        self.apptools.swipe(0.5, 0.3, 0.5, 0.8)
        try:
            self.find_element("//android.widget.TextView[@text='屏幕录制']").click()
            time.sleep(3)
        except:
            pass

    def element_point(self, el):
        start_x = int(el.location['x'])
        start_y = int(el.location['y'])
        width = int(el.size.get('width'))
        height = int(el.size.get('height'))
        x = start_x + width / 2
        y = start_y + height / 2
        return x, y

    def getVideo(self, duration):
        if self.apptools.device in apptool.huwei_device:
            os.system(
                self.apptools.ADB_PATH + '-s ' + self.apptools.device + ' shell rm /storage/emulated/0/Pictures/Screenshots/*.mp4')
            self.apptools.swipe(0.5, 0.01, 0.5, 0.8)
            time.sleep(0.5)
            self.apptools.swipe(0.5, 0.2, 0.5, 0.8)
            time.sleep(0.5)
            element = None
            for retryCount in range(1, 4):
                element = self.find_element("//android.widget.TextView[@text='屏幕录制']")
                if not element:
                    LOGGING.warn("Didn't find 屏幕录制 after %d times trial" % retryCount)
                    time.sleep(0.5)
            if not element:
                LOGGING.error("Didn't find 屏幕录制 in the end." + self.batch_num + self.app)
                return False
            try:
                element.click()
                time.sleep(3)
                LOGGING.debug("Start recording for huawei: " + self.apptools.device + ", " + self.apptools.scene)
            except Exception, e:
                LOGGING.exception("error occurs in getVideo " + self.apptools.device + ", " + self.apptools.scene)
                return False
        else:
            w, h = self.apptools.window_size()
            # Watch out! A bug may be caused by this way of recording.
            subprocess.Popen(self.apptools.ADB_PATH + "-s " + self.apptools.device +
                             " shell screenrecord --size " + str(w) + "x" + str(
                h) + " --time-limit " + str(duration) + " /sdcard/screenrecord.mp4",
                             stdout=subprocess.PIPE,
                             shell=True)
            LOGGING.debug("Start recording for NOT huawei: " + self.apptools.device + ", " + self.apptools.scene)
        return True

    def saveVideo(self):
        videoName = "video"
        tmp_save = os.path.join(os.path.join(constants.AUTO_PATH, self.apptools.device), self.apptools.scene)
        if not os.path.exists(tmp_save):
            os.makedirs(tmp_save)

        cur_path = os.getcwd()
        os.chdir(tmp_save)

        if self.apptools.device in constants.huawei_device:
            self.apptools.click_at(100, 30)
            LOGGING.debug('Recoding finished in HUAWEI device ' + self.apptools.device + ", " + self.apptools.scene)
            time.sleep(1)
            lines = os.popen(
                self.apptools.ADB_PATH + "-s " + self.apptools.device + " shell ls /storage/emulated/0/Pictures/Screenshots/*.mp4").readlines()
            for line in lines:
                if '.mp4' in line:
                    file_name = line.strip().split('/')[-1]
                    os.system(
                        self.apptools.ADB_PATH + "-s " + self.apptools.device + " pull /storage/emulated/0/Pictures/Screenshots/" +
                        file_name + " " + tmp_save + "/" + videoName + ".mp4")
                    break
        else:
            os.system(self.apptools.ADB_PATH + "-s " + self.apptools.device + " pull /sdcard/screenrecord.mp4 "
                      + tmp_save + "/" + videoName + ".mp4")
        ffmpeg_cmd = 'ffmpeg -i ' + videoName + '.mp4 -r 30 -f image2 image-%3d.jpg'
        # video_length = "ffmpeg -i demo.mp4 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
        os.system(ffmpeg_cmd)
        os.chdir(cur_path)

        return tmp_save