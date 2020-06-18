# -*- encoding=utf8 -*-
__author__ = "jayce"

from airtest.core.api import *
import threading
from multiprocessing import Process
import os
import time
import numpy as np

def run_Record():
    mkdir(mkpath)
    os.system('/Users/jayce/Jayce-iOSPerformance/NewsPerformance/OutputFile/xrecord --quicktime --id="f94ae345c82dcef7a575b84db7e95aac05d85d90" --out  %s/1.mp4 --time="8"' %(mkpath))
def Launch():
    os.system('python -m airtest run /Users/jayce/Jayce-iOSPerformance/Case/NetEase/LaunchApp.air  --device iOS:///127.0.0.1:8100 --log  /Users/jayce/Desktop/Airtest')

for x in xrange(0,5):
    os.system('python /Users/jayce/Jayce-iOSPerformance/Case/NetEase/Pictures/Pictures.py')