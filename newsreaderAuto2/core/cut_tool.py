#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import os
import time
import imghdr
import sys
from cv import Template
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "...")))
from casePackage.utils import tools
from aircv import aircv
from aircv import cv2
import get_time
import base64
import numpy as np
from PIL import Image



def cut_image(image, x_1, y_1, x_2, y_2):
    image = aircv.imread(image)
    height, width, channels = image.shape
    return image[(height*x_1):(height*x_2), (width*y_1):(width*y_2)]

def _is_white_screen(file, w=4, h=6):
    end = '/home/jenkins/Source/lrp/baidu/searchbox-ep/lrp/res/chrome_search_query_baidu.png'
    count = 0
    image = aircv.imread(file)
    height, width, channels = image.shape
    image = image[100:height, 0:width]
    height, width, channels = image.shape
    white_image_tem = end.replace(end.split('/')[-1], 'chrome_search_query_baidu.png')
    print white_image_tem
    white_image_tem = aircv.imread(white_image_tem)
    h_2, w_2, cha = white_image_tem.shape
    if h_2 > height/h or w_2 > width/w:
        white_image_tem = white_image_tem[0:height/h, 0:width/w]
    tem = Template(white_image_tem, threshold=0.1, sift=False)
    for i in range(0, w):
        for j in range(0, h):
            m = image[(height * j / h):(height * (j + 1) / h), (width * i / w):(width * (i + 1) / w)]
            h_1, w_1, ch = m.shape
            h_2, w_2, cha = white_image_tem.shape
            if True:
                print '***********'
                print h_1, w_1
                print h_2, w_2
                print '***********'
            if tem.match_in(m):
                cv2.imshow(str(i) + "_" + str(j), m)
                cv2.waitKey()
            else:
                cv2.imshow('aaaaaaa', m)
                cv2.waitKey()

def _is_white_screen_1(file, w=4, h=6):
    end = '/home/jenkins/Source/lrp/baidu/searchbox-ep/lrp/res/end.png'
    count = 0
    image = aircv.imread(file)
    height, width, channels = image.shape
    image = image[100:height, 0:width]
    height, width, channels = image.shape
    white_image_tem = end.replace(end.split('/')[-1], 'white_image.png')
    print white_image_tem
    white_image_tem = aircv.imread(white_image_tem)
    for i in range(0, w):
        for j in range(0, h):
            m = image[(height * j / h):(height * (j + 1) / h), (width * i / w):(width * (i + 1) / w)]
            h_1, w_1, ch = m.shape
            h_2, w_2, cha = white_image_tem.shape
            if True:
                print '***********'
                print h_1, w_1
                print h_2, w_2
                print '***********'
            tem = Template(m, threshold=0.3, sift=False)
            if tem.match_in(white_image_tem):
                count += 1
                # cv2.imshow(str(i) + "_" + str(j), m)
                # cv2.waitKey()
            # else:
            #     cv2.imshow('aaaaaaa', m)
            #     cv2.waitKey()
            print count

def test(file, num=12, w=4, h=6, white='white_image.png'):
    end = '/home/jenkins/Source/lrp/baidu/searchbox-ep/lrp/res/end.png'
    count = 0
    if isinstance(file, type('')):
        image = aircv.imread(file)
    else:
        image = file
    image = Template.image_cut(image)
    height, width, channels = image.shape
    white_image_tem = end.replace(end.split('/')[-1], white)
    white_image_tem = aircv.imread(white_image_tem)
    ret, white_image_tem = cv2.threshold(white_image_tem, 50, 255, cv2.THRESH_BINARY)
    for i in range(0, w):
        for j in range(0, h):
            m = image[(height * j / h):(height * (j + 1) / h), (width * i / w):(width * (i + 1) / w)]
            ret, m = cv2.threshold(m, 50, 255, cv2.THRESH_BINARY)
            tem = Template(m, threshold=0.5, sift=True)
            if tem.match_in(white_image_tem):
                cv2.imshow('aa', m)
                cv2.waitKey()
                count += 1
            else:
                cv2.imshow('bb', m)
                cv2.waitKey()
    print count


def resizeImg(srcFile):
    sImg = Image.open(srcFile)
    w, h = sImg.size
    print w, h
    dImg = sImg.resize((w / 2, h / 2), Image.ANTIALIAS)  # 设置压缩尺寸和选项，注意尺寸要用括号
    return dImg
    # dImg.save(dstFile)  # 也可以用srcFile原路径保存,或者更改后缀保存，save这个函数后面可以加压缩编码选项JPEG之类的
    # print dstFile + " compressed succeeded"


if __name__ == "__main__":
    cv2.imshow('aaa', cut_image('/home/jenkins/video/bd3ea87f/feed_shipin_pinglun/image-063.jpg', 0.5, 0, 1.0, 1.0))
    cv2.waitKey()
    # image = '/home/jenkins/video/bd3ea87f/image_list/image-119.jpg'
    # file = open(image, 'rb')
    # imagebase = base64.b64encode(file.read())
    # print imagebase
    # print len(imagebase)
    # imgData = base64.b64decode(imagebase)
    # nparr = np.fromstring(imgData, np.uint8)
    # img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
    # cv2.imshow('aa', img)
    # cv2.waitKey()
    # res = cv2.resize(img, (270, 480), interpolation=cv2.INTER_AREA)
    # cv2.imshow('bb', res)
    # cv2.waitKey()
    # cv2.imwrite('/home/jenkins/bbb.png', res)
    # file = open('/home/jenkins/bbb.png', 'rb')
    # imagebase = base64.b64encode(file.read())
    # print imagebase
    # print len(imagebase)
    # # cv2.imwrite('/home/jenkins/Source/lrp/baidu/searchbox-ep/lrp/res/toutiao_feed_tab.png', cut_image('/home/jenkins/video/bd3ea87f/feed_tab/image-044.jpg', 0.5, 0, 1.0, 1.0))
    # # _is_white_screen_1('/home/jenkins/video/bd3ea87f/start_cool_feed/image-114.jpg')
    # # test('/home/jenkins/video/bd3ea87f/search_query/image-089.jpg')
    # tem = Template('/home/jenkins/Source/lrp/baidu/searchbox-ep/lrp/res/end.png', threshold=0.9, sift=True)
    # tem.match_in('/home/jenkins/video/bd3ea87f/start_cool_feed/image-072.jpg')