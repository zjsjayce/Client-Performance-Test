# -*- encoding=utf8 -*-
__author__ = "jayce"

from airtest.core.api import *
import threading
from multiprocessing import Process
import os
from poco.drivers.ios import iosPoco
import time

sleep(1.0)
start_app('com.ss.iphone.article.News')
sleep(7.0)
poco = iosPoco()
poco("图片").click()
sleep(3.0)