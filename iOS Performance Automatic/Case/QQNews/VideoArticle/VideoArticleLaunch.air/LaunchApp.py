# -*- encoding=utf8 -*-
__author__ = "jayce"

from airtest.core.api import *

sleep(1.0)
start_app('com.netease.newspro')
sleep(1.0)
touch((455,2110))
sleep(1.0)

auto_setup(__file__)
