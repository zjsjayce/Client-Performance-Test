# -*- encoding=utf8 -*-
__author__ = "jayce"
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from airtest.core.api import *
import threading
from multiprocessing import Process
import os
import time

sleep(1.0)
touch((567,741))
sleep(2.0)
touch((57,129))