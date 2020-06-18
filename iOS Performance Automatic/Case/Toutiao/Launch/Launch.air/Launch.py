# -*- encoding=utf8 -*-
__author__ = "jayce"

from airtest.core.api import *

sleep(1.0)
start_app('com.ss.iphone.article.News')
sleep(2.0)
stop_app('com.ss.iphone.article.News')
auto_setup(__file__)
