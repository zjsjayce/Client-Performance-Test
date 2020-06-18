# -*- encoding=utf8 -*-
__author__ = "jayce"

import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from airtest.core.api import *

sleep(1.0)
start_app('com.netease.newspro')
sleep(2.0)
auto_setup(__file__)
