# -*- encoding=utf8 -*-
__author__ = "jayce"

from airtest.core.api import *
import threading
from multiprocessing import Process
import os
from poco.drivers.ios import iosPoco
import time

poco = iosPoco()
def run_Record():
    time_now = int(time.time())
    mkpath ="/Users/jayce/PerformanceOutput/NetEase/Article/%s" %(time_now)
    mkdir(mkpath)
    os.system('/Users/jayce/Jayce-iOSPerformance/NewsPerformance/OutputFile/xrecord --quicktime --id="f94ae345c82dcef7a575b84db7e95aac05d85d90" --out  %s/1.mp4 --time="8"' %(mkpath))
def run_proc():
    touch((567,741))
    sleep(2.0)
    touch((57,129))
def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        #print path+' 创建成功'
        return True
    else:
        #print path+' 目录已存在'
        return False
start_app('com.netease.news')
sleep(3.0)
for x in xrange(1,10):
    a = Process(target=run_Record)
    b = Process(target=run_proc)
    a.start()
    sleep(1.0)
    b.start()
    a.join()
    sleep(4.0)
    pass

stop_app('com.netease.news')