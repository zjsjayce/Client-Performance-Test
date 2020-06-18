# -*- encoding=utf8 -*-
__author__ = "jayce"

from airtest.core.api import *
sleep(3.0)
start_app('com.netease.newsent')
sleep(10.0)
touch((423,1232))
sleep(10.0)
touch((423,1232))
stop_app('com.netease.newsent')


auto_setup(__file__)