#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import threading
import os
import sys
import csv
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import Utils.exception as exception
from cv import Template

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import casePackage.utils.tools as tools
import casePackage.utils.constants as constants
from aircv import aircv
from aircv import cv2
import shutil
# from bos import bos
import Utils.logger as logger

# LOGGING = logger.Logger().get_logger(__name__)
LOGGING = logger.get_logger(__name__)
parser = argparse.ArgumentParser()
parser.add_argument("--path", help="the path of screenshots")
parser.add_argument("--methods", help="the json of image process methods", nargs="+")
parser.add_argument("--scene", help="the scene of test")

def arguments_check():
    def make_wrapper(func):
        def wrapper(*args, **kwargs):
            code = func.func_code
            names = list(code.co_varnames[:code.co_argcount])
            if len(args) < 2:
                pass
            else:
                if not args[names.index('self')].file_list:
                    raise Exception(str(args[names.index('self')].__class__) + ' did not init!')
                start = args[names.index('start')]
                end = len(args[names.index('self')].file_list) - 1
                if isinstance(start, int):
                    if start < 0 or start > end or end == 0:
                        raise Exception('fountion: ' + func.__name__ + ' para error!')
                else:
                    raise Exception('fountion: ' + func.__name__ + ' para type error!')
            return func(*args, **kwargs)

        return wrapper

    return make_wrapper


def get_dominant_color(image):
    """
    获取图片的main color
    """

    import colorsys
    from PIL import Image
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if image:
        # image = Image.open(image)
        image = image.convert('RGBA')
        (x, y) = image.size
        if x * y > 200 * 200:
            image.thumbnail((200, 200))

        max_score = 0
        dominant_color = 0

        for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
            # if a == 0:
            #     continue

            saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
            y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
            y = (y - 16.0) / (235 - 16)
            # if y > 0.9:
            #     continue
            score = (saturation + 0.1) * count

            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)

        return dominant_color


class Get_time(threading.Thread):
    def __init__(self, suite, ran, batch_num, device, scene, test_file_path, tmp_save, result_biz_dir,
                 method_dicts=None, plugin=False):
        threading.Thread.__init__(self)
        self.ran = ran
        self.suite = suite
        self.batch_num = batch_num
        self.device = device
        self.scene = scene
        self.test_file_path = test_file_path
        self.tmp_save = tmp_save
        self.result_biz_dir = result_biz_dir
        self.file_list = None
        self.method_dicts = method_dicts
        self.time = 0
        self.log_tag = self.batch_num + ': ' + 'scene: ' + self.scene + ', device: ' + self.device + \
                       ', result_biz_dir: ' + self.result_biz_dir.split('\\')[-1]
        self.plugin = plugin
        self.bSuccess = False

    def _init_file_list(self):
        if self.file_list == None:
            self.file_list = os.listdir(self.tmp_save)
            self.file_list.sort(self.compare)
            remove_list = []
            for image in self.file_list:
                if not image.__contains__(".jpg"):
                    remove_list.append(image)
            for image_toremove in remove_list:
                self.file_list.remove(image_toremove)
            for image in self.file_list:
                self.file_list[self.file_list.index(image)] = os.path.join(self.tmp_save, image)

    def compare(self, x, y):
        DIR = self.tmp_save
        stat_x = os.stat(DIR + "/" + x)
        stat_y = os.stat(DIR + "/" + y)
        if stat_x.st_mtime > stat_y.st_mtime:
            return 1
        elif stat_x.st_mtime < stat_y.st_mtime:
            return -1
        else:
            return 0

    @staticmethod
    def _cut_image(image, x_1, y_1, x_2, y_2):
        image = aircv.imread(image)
        height, width, channels = image.shape
        return image[(int)(height * x_1):(int)(height * x_2), (int)(width * y_1):(int)(width * y_2)]

    @arguments_check()
    def _find_video_play_from_landing_page(self, start, x_1=0.05, y_1=0.01, x_2=0.3, y_2=0.99, threshold=None):
        """
        :param start:
        :param x_1:
        :param y_1:
        :param x_2:
        :param y_2:
        :return:
        """
        return self._find_diff_by_area_change(start, x_1, y_1, x_2, y_2, threshold or self.threshold_2)

    @arguments_check()
    def find_netease_shouzhen(self, start, x_1=0.05, y_1=0.15, x_2=0.95, y_2=0.45, threshold=None):
        return self._find_diff_by_area_change(start, x_1, y_1, x_2, y_2, threshold or self.threshold_2)

    # @arguments_check()
    def _find_diff_by_area_change(self, start, x_1, y_1, x_2, y_2, threshold=None):
        """
                寻找从静到动的点.前后两张图片对比,如果n+1与n不同,则返回n+1
                :param start:
                :param x_1:
                :param y_1:
                :param x_2:
                :param y_2:
                :return:
                """
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            image = self._cut_image(self.file_list[i], x_1, y_1, x_2, y_2)
            screen = self._cut_image(self.file_list[i + 1], x_1, y_1, x_2, y_2)
            t = Template(image, threshold=threshold or 0.8, sift=False)
            if not t.match_in(screen):
                return i + 1

    # @arguments_check()
    def _find_diff_by_area_change_from_back(self, start, x_1=0.65, y_1=0.53, x_2=0.95, y_2=0.85, threshold=0.999):
        """
                寻找从静到动的点.前后两张图片对比,如果n+1与n不同,则返回n+1
                :param start:
                :param x_1:
                :param y_1:
                :param x_2:
                :param y_2:
                :return:
                """
        i = len(self.file_list) - 2
        while i > start:
            print self.file_list[i]
            image = self._cut_image(self.file_list[i], x_1, y_1, x_2, y_2)
            screen = self._cut_image(self.file_list[i - 1], x_1, y_1, x_2, y_2)
            t = Template(image, threshold=threshold or 0.8, sift=False)
            if not t.match_in(screen):
                return i
            i -= 1

    @arguments_check()
    def tieba_video_middle_start(self, start):
        return self._find_diff_by_area_change(start, 0.95, 0.0, 1.0, 1.0, self.threshold_1)

    @arguments_check()
    def video_loading_page_white(self, start, x_1=0.7, y_1=0.001, x_2=0.9, y_2=0.5):
        """
        判断视频落地页加载完成,相关推荐空白
        :param start:
        :param x_1:
        :param y_1:
        :param x_2:
        :param y_2:
        :return:
        """
        for i in range(start, len(self.file_list) - 2):
            print self.file_list[i]
            image = self._cut_image(self.file_list[i], x_1, y_1, x_2, y_2)
            if self._is_white_screen(image, num=0.9):
                return i

    @arguments_check()
    def _check_grey_loading_page(self, start, image='feed_shipin_loading.png'):
        # 判断是不是出现了灰图
        image = self.end.replace(self.end.split('/')[-1], image)
        t = Template(image, threshold=0.9, sift=False)
        if t.match_in(self.file_list[start]):
            end = self.end
            self.end = image
            num = self._find_by_image_dis(start, threshold=0.9)
            self.end = end
            return num
        return start

    def check_grey_loading_page_p10(self, start):
        return self._check_grey_loading_page(start, image='feed_shipin_grey_p10.png')

    def search_query_result(self, start):
        start = self.find_by_change(start)
        if self._is_white_screen(self.file_list[start]):
            return self._find_white_screen_dis(start)

    @arguments_check()
    def check_video_player_black(self, start, image='video_player_black.png'):
        """
        头条相关推荐打开视频,播放器开始播放之前有一段黑屏逐渐变亮的过程.真恶心.特别适配
        :param start:
        :param image:
        :return:
        """
        start = self._find_video_play_from_landing_page(start)
        image = self.end.replace(self.end.split('/')[-1], image)
        t = Template(image, threshold=0.99, sift=True)
        if t.match_in(self.file_list[start]):
            return self._find_video_play_from_landing_page(start + 1, threshold=0.7)
        return start

    @arguments_check()
    def check_video_player_black_p10(self, start, image='video_player_black_p10.png'):
        return self.check_video_player_black(start, image=image)

    # @arguments_check()
    def _find_by_image(self, start, threshold, sift, filename, is_image_cut):
        """
        当image出现时返回
        :param start:
        :return:
        """
        fileWholeName = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
                                     'res/' + filename.split('/')[-1])
        tem = Template(fileWholeName, threshold=threshold, sift=sift, is_image_cut=is_image_cut)
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            if tem.match_in(self.file_list[i]):
                return i
        return False

    def _is_white_screen(self, file, num=0.6, w=10, h=10, black=False):
        """
        file超过一般区域为空白,返回True,否则返回False
        :param file:
        :param num:
        :param w:
        :param h:
        :return:
        """
        count = 0
        if isinstance(file, type('')):
            image = aircv.imread(file)
        else:
            image = file
        image = Template.image_cut(image)
        # ret, image = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)
        height, width, channels = image.shape
        for i in range(0, w):
            for j in range(0, h):
                m = image[(height * j / h):(height * (j + 1) / h), (width * i / w):(width * (i + 1) / w)]
                if self._is_white_screen_by_point(m, black):
                    count += 1
        print str(float(count) / float(w * h)) + " is white"
        return float(count) / float(w * h) > num

    def _is_red_screen(self, file, num=0.6, w=10, h=10, black=False):
        """
        file超过一般区域为网易红,返回True,否则返回False
        :param file:
        :param num:
        :param w:
        :param h:
        :return:
        """
        count = 0
        if isinstance(file, type('')):
            image = aircv.imread(file)
        else:
            image = file
        image = Template.image_cut(image)
        # ret, image = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)
        height, width, channels = image.shape
        for i in range(0, w):
            for j in range(0, h):
                m = image[(height * j / h):(height * (j + 1) / h), (width * i / w):(width * (i + 1) / w)]
                if self._is_red_screen_by_point(m, black):
                    count += 1
        print str(float(count) / float(w * h)) + " is white"
        return float(count) / float(w * h) > num

    def _is_white_screen_by_point(self, image, black=False):
        r, g, b = get_dominant_color(image)
        if isinstance(image, type('')):
            image = aircv.imread(image)
        height, width, channels = image.shape
        image = cv2.resize(image, (height / 10, width / 10), interpolation=cv2.INTER_CUBIC)
        height, width, channels = image.shape
        for k in range(0, height):
            for l in range(0, width):
                x, y, z = image[k, l]
                if x >= b * 0.95 and x <= b * 1.05 and y >= g * 0.95 and y <= g * 1.05 and z >= r * 0.95 and z <= r * 1.05:
                    continue
                else:
                    return False
        return True

    def _is_red_screen_by_point(self, image, black=False):
        r, g, b = get_dominant_color(image)
        if isinstance(image, type('')):
            image = aircv.imread(image)
        height, width, channels = image.shape
        image = cv2.resize(image, (height / 10, width / 10), interpolation=cv2.INTER_CUBIC)
        height, width, channels = image.shape
        for k in range(0, height):
            for l in range(0, width):
                x, y, z = image[k, l]
                if x >= b * 0.95 and x <= b * 1.05 and y >= g * 0.95 and y <= g * 1.05 and z >= r * 0.95 and z <= r * 1.05:
                    continue
                else:
                    return False
        return True

    @arguments_check()
    def find_white_screen(self, start, threshold):
        """
        正序找到屏幕超过threshold为空白的一张图片时,返回
        :param start:
        :return:
        """
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            if self._is_white_screen(self.file_list[i], threshold):
                return i
        return False

    # @arguments_check()
    # def find_white_screen_more(self, start, threshold, is_image_cut=False, sift=False):
    #     """
    #     正序找到屏幕超过一般为空白的一张图片时,返回
    #     :param start:
    #     :return:
    #     """
    #     for i in range(start, len(self.file_list) - 1):
    #         print self.file_list[i]
    #         if self._is_white_screen(self.file_list[i], threshold):
    #             return i
    #     return False

    @arguments_check()
    def find_red_screen_more(self, start):
        """
        正序找到屏幕超过一般为空白的一张图片时,返回
        :param start:
        :return:
        """
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            if self._is_red_screen(self.file_list[i], num=0.8):
                return i
        return False
    #
    # # @arguments_check()
    # def _find_white_screen_dis_more(self, start, threshold):
    #     """
    #     正序查找,第一张非屏幕超过一半为空白的图片时返回
    #     :param start:
    #     :return:
    #     """
    #     for i in range(start, len(self.file_list) - 1):
    #         print self.file_list[i]
    #         if not self._is_white_screen(self.file_list[i], threshold):
    #             return i
    #     return False

    @arguments_check()
    def _find_white_screen_dis(self, start, threshold):
        """
        正序查找,第一张非屏幕超过一半为空白的图片时返回
        :param start:
        :return:
        """
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            if not self._is_white_screen(self.file_list[i], threshold):
                return i
        return False


    @arguments_check()
    def _find_white_screen_dis_by_area(self, start, threshold, x_1, y_1, x_2, y_2):
        """
        正序查找,第一张非屏幕超过一半为空白的图片时返回
        :param start:
        :return:
        """
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            image = self._cut_image(self.file_list[i], x_1, y_1, x_2, y_2)
            if not self._is_white_screen(image, threshold):
                return i
        return False

    # @arguments_check()
    # def _find_white_screen_dis_less(self, start, threshold):
    #     """
    #     正序查找,第一张非屏幕超过一半为空白的图片时返回
    #     :param start:
    #     :return:
    #     """
    #     for i in range(start, len(self.file_list) - 1):
    #         print self.file_list[i]
    #         if not self._is_white_screen(self.file_list[i], num=threshold):
    #             return i
    #     return False

    @arguments_check()
    def find_white_screen_gentie(self, start, threshold=None):
        """
        正序查找,第一张非屏幕超过一半为空白的图片时返回
        :param start:
        :return:
        """
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            image_cut = self._cut_image(self.file_list[i], 0.56
                                        , 0.87, 0.95, 0.92)
            if not self._is_white_screen(image_cut, 0.6, 1, 1, False):
                return i
        return False

    def _is_black_screen(self, file):
        return self._is_white_screen(file, black=True)

    @arguments_check()
    def _find_black_screen(self, start):
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            if self._is_black_screen(self.file_list[i]):
                return i
        return False

    @arguments_check()
    def _find_black_screen_dis(self, start):
        """
        正序查找,第一张非屏幕超过一半为空白的图片时返回
        :param start:
        :return:
        """
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            if not self._is_black_screen(self.file_list[i]):
                return i
        return False

    @arguments_check()
    def _start_feed(self, start):
        """
            判断首页feed列表页是否为空白.空白的话正序寻找空白消失的图片返回
        :param start:
        :param x_1:
        :param y_1:
        :param x_2:
        :param y_2:
        :return:
        """
        for i in range(start, len(self.file_list) - 2):
            print self.file_list[i]
            if not self._is_white_screen(self.file_list[i], num=0.6):
                return i

    @arguments_check()
    def _start_feed_night(self, start):
        """
            判断首页feed列表页是否为空白.空白的话正序寻找空白消失的图片返回
        :param start:
        :param x_1:
        :param y_1:
        :param x_2:
        :param y_2:
        :return:
        """
        for i in range(start, len(self.file_list) - 2):
            print self.file_list[i]
            if not self._is_black_screen(self.file_list[i]):
                return i

    @arguments_check()
    def _find_by_image_dis(self, start, threshold=None):
        """
        要找的图片消失时返回
        :param start:
        :return:
        """
        tem = Template(self.end, threshold=threshold or self.threshold_2, sift=self.sift)
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            if not tem.match_in(self.file_list[i]):
                return i
        return False

    @arguments_check()
    def _find_first_frame(self):
        """
        根据帧率变化寻找起点
        :return:
        """
        pass

    def _find_diff_from_point_to_front(self, start, threshold=None):
        """
        从start点往前找diff
        :param start:
        :param threshold:
        :return:
        """
        while start > 0:
            start -= 1
            print self.file_list[start]
            tem = Template(self.file_list[start], threshold=threshold or self.threshold_2,
                           is_image_cut=self.comp_previous_1, sift=False)
            if not tem.match_in(self.file_list[start - 1]):
                return start

    def _find_diff_from_back_to_front(self, start, threshold, is_image_cut, sift):
        """
        从最后一张开始往前找diff
        :param start:
        :return:
        """
        i = len(self.file_list) - 4
        while i > start:
            print self.file_list[i]
            tem = Template(self.file_list[i], threshold=threshold, is_image_cut=is_image_cut, sift=sift)
            if not tem.match_in(self.file_list[i - 1]) and not tem.match_in(self.file_list[i - 2]) and not tem.match_in(
                    self.file_list[i - 3]):
                return i
            i -= 1

    def _find_image_from_back_to_front(self, start, ):
        """
                从后往前,当image出现时返回
                :param start:
                :return:
                """
        i = len(self.file_list) - 2
        while i > start:
            print self.file_list[i]
            tem = Template(self.end, threshold=self.threshold_2, sift=self.sift)
            if tem.match_in(self.file_list[i]):
                return i
            i -= 1
        return False

    @arguments_check()
    def _find_by_text(self, start):
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            print self.end.split('/')[-1]
            if tools.get_text_from_image(self.file_list[i], self.end.split('/')[-1]):
                return i

    @arguments_check()
    def _find_by_text_dis(self, start):
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            if not tools.get_text_from_image(self.file_list[i], self.end.split('/')[-1]):
                return i

    # @arguments_check()
    def find_start_action_by_change(self, start, threshold=None, is_image_cut=False, sift=False):
        """
        发生变化时返回
        :param start:
        :return:
        """
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            tem = Template(self.file_list[i], threshold=threshold, is_image_cut=is_image_cut, sift=sift)
            if not tem.match_in(self.file_list[i + 1]):
                return i + 1

    def _find_by_change_stop(self, start, threshold, is_image_cut):
        """
        停止变化时返回
        :param start:
        :return:
        """
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            tem = Template(self.file_list[i], threshold=threshold,
                           is_image_cut=is_image_cut, sift=False)
            if tem.match_in(self.file_list[i + 1]) and tem.match_in(self.file_list[i + 2]):
                return i

    def _find_by_area_change_stop(self, start, x_1, y_1, x_2, y_2, threshold, is_image_cut):
        """
        停止变化时返回
        :param start:
        :return:
        """
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            image = self._cut_image(self.file_list[i], x_1, y_1, x_2, y_2)
            screen = self._cut_image(self.file_list[i + 1], x_1, y_1, x_2, y_2)
            tem = Template(image, threshold=threshold,
                           is_image_cut=is_image_cut, sift=False)
            if tem.match_in(screen):
                return i

    def find_by_change(self, start):
        return self.find_start_action_by_change(start, threshold=self.threshold_2)

    def find_change_from_first_page(self, start):
        tem = Template(self.file_list[0], threshold=self.threshold_2, sift=False, is_image_cut=True)
        for i in range(start, len(self.file_list) - 1):
            print self.file_list[i]
            if not tem.match_in(self.file_list[i]):
                return i
        return False

    # @arguments_check()
    # def _from_chang_to_stop(self, start, x_1=0.5, y_1=0, x_2=1.0, y_2=1.0):
    #     for i in range(start + 3, len(self.file_list) - 1):
    #         image_1 = self._cut_image(self.file_list[i], x_1, y_1, x_2, y_2)
    #         image_2 = self._cut_image(self.file_list[i-3], x_1, y_1, x_2, y_2)
    #         t = Template(image_1, threshold=0.99, sift=False)
    #         if t.match_in(image_2):
    #             return i - 2

    @arguments_check()
    def _video_start_from_list(self, start):
        """
        列表页上寻找起播时间. end为一张特殊图片,少数case在起播之前会出现一张灰图,需要找到并跳过这张配图,再计算起播时间.
        :param start:
        :return:
        """
        num = self.find_start_action_by_change(start, threshold=self.threshold_2)
        # 判断是不是出现了灰图
        t = Template(self.end, threshold=self.threshold_2, sift=False)
        if t.match_in(self.file_list[num]):
            num = self._find_by_image_dis(num)
            return self.find_start_action_by_change(num, threshold=self.threshold_2)
        return num

    def _update_end_image(self, num):
        self.end = self._cut_image(self.file_list[-1], 0.4, 0.01, 0.6, 1.0)
        return num

    @arguments_check()
    def _find_start_action_by_oprtion_change(self, start, threshold=None):
        """
                局部发生变化时返回
                :param start:
                :return:
                """
        return self._find_diff_by_area_change(start, 0.5, 0, 1.0, 1.0, self.threshold_1)

    def result_save(self, mile_stone):
        # bos_client = bos.Bucket()
        if not mile_stone:
            return
        root = os.path.join(os.environ['HOMEPATH'], 'video')
        # TIME = str(time.ctime(os.path.getctime(self.tmp_save)))
        path = os.path.join(root, self.result_biz_dir)
        if not os.path.exists(path):
            os.makedirs(path)
        shutil.copy(os.path.join(self.tmp_save, "video.mp4"), path)
        for point in mile_stone:
            shutil.copy(self.file_list[point - 1], path)
            shutil.copy(self.file_list[point + 1], path)
            shutil.copy(self.file_list[point], path)
        # self.test_file.write("dataSourceDir: " + "performance" + self.result_biz_dir.split("performance")[1] + '\n')
        shutil.copy(self.test_file_path, path)

    def run(self):
        start = 20
        self._init_file_list()
        try:
            # if self.start_method:
            #     end_para = self.threshold_2
            #     end_key = self.end
            #     self.threshold_2 = self.threshold_1
            #     self.end = self.start_i
            #     start = getattr(self, self.method_dicts[0])(10)
            #     print(self.log_tag + ': ***start method:' + self.method_dicts[0])
            #     self.threshold_2 = end_para
            #     self.end = end_key
            #     self.method_dicts.pop(0)
            # else:
            #     start = self.find_start_action_by_change(10)
            #     print(self.log_tag + ': ***start method: _find_start_action_by_change')
            # print(self.log_tag + ': ***start:' + str(start))
            end = start
            mile_stone = []

            for method in self.method_dicts:
                # collect the func and its argument
                method_name = method[constants.MethodField.MethodName.value]
                method.pop(constants.MethodField.MethodName.value)
                add_to_milestone = method[constants.MethodField.AddToMilestone.value]
                method.pop(constants.MethodField.AddToMilestone.value)
                func_args = {}
                for k, v in method.items():
                    func_args[k] = v
                if not hasattr(self, method_name):
                    raise Exception('no method found error!')

                # execute the specific func
                end = getattr(self, method_name)(start=end, **func_args)

                # collect the test result of this func
                if add_to_milestone and end:
                    mile_stone.append(end)
                print self.log_tag + ': ' + '***' + str(method_name) + str(end) + str(add_to_milestone)
                print(self.log_tag + ': ' + str(method_name) + str(end) + str(add_to_milestone))
        except Exception, e:
            raise exception.CaseExecutingException("exception when invoke find func in get_time", e)

        # After all the funcs have been executed, compute time costs using mile_stone
        self.computeAndRecordTotal(mile_stone)
        if (not self.plugin):
            self.result_save(mile_stone)
        if (self.time == 0 or not self.bSuccess):
            LOGGING.error(self.log_tag + " There's something wrong in get_time.")
            print(self.log_tag + " There's something wrong in get_time.")
        return self.bSuccess

    def computeAndRecordTotal(self, mile_stone):
        cur_path = paths
        os.chdir(cur_path)
        pathout = os.path.abspath(os.path.join(os.getcwd(), "../.."))
        os.chdir(pathout)
        if "start" in self.scene:
            if len(mile_stone) == 3:
                self.bSuccess = True
                white = (mile_stone[1] - mile_stone[0]) * 33.3
                self.time = (mile_stone[2] - mile_stone[0]) * 33.3
                with open(self.test_file_path, 'a') as logFile:
                    logFile.write('white: ' + str(white) + '\n')
                    logFile.write('total: ' + str(self.time) + '\n')
                    print "white" + str(white)
                    print "total" + str(self.time)
                    print "Picturelist" + str(mile_stone)
                self.ran.get(self.suite).get(self.scene).append([white, self.time])
            if len(mile_stone) == 2:
                # print("milestone: " + str(mile_stone))
                print("milestone: " + str(mile_stone))
                self.bSuccess = True
                self.time = (mile_stone[1] - mile_stone[0]) * 33.3
                white = (mile_stone[1] - mile_stone[0]) * 33.3
                mile_stone[2] = mile_stone[1]
                with open(self.test_file_path, 'a') as logFile:
                    logFile.write('total: ' + str(self.time) + '\n')
                    print str(self.time)
                print "white" + str(white)
                print "total" + str(self.time)
                print "Picturelist" + str(mile_stone)
                self.ran.get(self.suite).get(self.scene).append(self.time)

            with open("Performance.csv", "a") as datacsv:
                csvwriter = csv.writer(datacsv, dialect=("excel"))
                csvwriter.writerow([self.scene, paths, white, self.time, mile_stone[0], mile_stone[1], mile_stone[2]])
        else:
            print("milestone: " + str(mile_stone))
            self.bSuccess = True
            self.time = (mile_stone[1] - mile_stone[0]) * 33.3
            if "list_refresh" in self.scene:
                self.time = self.time - 33.3*3
            with open(self.test_file_path, 'a') as logFile:
                logFile.write('total: ' + str(self.time) + '\n')
                print str(self.time)
            with open("Performance.csv", "a") as datacsv:
                csvwriter = csv.writer(datacsv, dialect=("excel"))
                csvwriter.writerow([self.scene,paths,self.time,mile_stone[0], mile_stone[1]])
        cur_path = "/Users/jayce/netease/jenkins/workspace/iOS-Performance-Test/CSV"
        os.chdir(cur_path)
        if "start" in self.scene:
            with open("iOS_2020_coldstart-white_netease-test.csv", "a") as datacsv:
                csvwriter = csv.writer(datacsv, dialect=("excel"))
                csvwriter.writerow(white)
            with open("iOS_2020_coldstart-total_netease-test.csv", "a") as datacsv:
                csvwriter = csv.writer(datacsv, dialect=("excel"))
                csvwriter.writerow([self.time])
        if "list_refresh" in self.scene:
            with open("iOS_2020_list-refresh_netease-test.csv", "a") as datacsv:
                csvwriter = csv.writer(datacsv, dialect=("excel"))
                csvwriter.writerow([self.time])
        if "tuwen" in self.scene:
            with open("iOS_2020_tuwen_netease-test.csv", "a") as datacsv:
                csvwriter = csv.writer(datacsv, dialect=("excel"))
                csvwriter.writerow([self.time])
        if "tuji" in self.scene:
            with open("iOS_2020_tuji_netease-test.csv", "a") as datacsv:
                csvwriter = csv.writer(datacsv, dialect=("excel"))
                csvwriter.writerow([self.time])







if __name__ == "__main__":
    args = parser.parse_args()
    if args.methods and args.path and args.scene:
        paths = args.path
        scene = args.scene
        method_dicts = [ eval(method) for method in args.methods]
    else:
        paths = [r'C:\Users\zhaoyuting\Desktop\f\H4Htmp']
        method_dicts = [
                          {
                              "method_name": "find_start_action_by_change",
                              "threshold": 0.9975,
                              "add_to_milestone": True,
                              "sift": False,
                              "is_image_cut": True
                          },
                          {
                              "method_name": "_find_diff_by_area_change",
                              "threshold": 0.97,
                              "add_to_milestone": True,
                              "x_1": 0.05,
                              "y_1": 0.15,
                              "x_2": 0.95,
                              "y_2": 0.45
                          }
      ]
    print paths, method_dicts
    i = 0
    for tmp_save in paths.split():
        i += 1
        gt = Get_time(plugin=True, suite="netease_grey_biz", ran={}, batch_num='test', device="aaa",
                      scene=scene, test_file_path='D:\\testGetTime' + str(i) + '.txt',
                      tmp_save=tmp_save, result_biz_dir='',
                      method_dicts=method_dicts)
        if gt.suite not in gt.ran.keys():
            gt.ran.update({
                gt.suite: {}
            })
        if gt.scene not in gt.ran.get(gt.suite):
            gt.ran.get(gt.suite).update({
                gt.scene: []
            })
        # image = Get_time._cut_image('D:\\Users\\snoop\\video\\XPU4C17112010268\\netease_tuwen\\image-206.jpg', 0.05, 0.87,
        #                            0.95, 0.92)
        # print gt._is_white_screen(r'C:\Users\zhaoyuting\Desktop\f\H2Htmp\image-195.jpg', num=0.5)
        gt.run()
