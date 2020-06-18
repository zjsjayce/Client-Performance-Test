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
def EndApp():
    os.system('python -m airtest run /Users/jayce/Jayce-iOSPerformance/Case/NetEase/EndApp.air  --device iOS:///127.0.0.1:8100 --log  /Users/jayce/Desktop/Airtest')
def run_proc():
    os.system('python -m airtest run /Users/jayce/Jayce-iOSPerformance/Case/NetEase/Refresh-toutiao/Refresh-toutiao.air  --device iOS:///127.0.0.1:8100 --log  /Users/jayce/Desktop/Airtest')
def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print path + ' 创建成功'
        return True
    else:
        print path + ' 目录已存在'
        return False
def fenzhen(path):
    half1 = 'ffmpeg -i %s/1.mp4  -r 30 -f image2 image-' %(path)
    half2 = '%3d.jpg' 
    whole = '%s%s' %(half1,half2)
    os.system('%s' %(whole))
    print whole
def CV(path):
    half1 = "{           'method_name': 'find_start_action_by_change',           'threshold': 0.7,           'add_to_milestone': True,           'sift': False,           'is_image_cut': True         }"
    half2 = "{           'method_name': '_find_by_image',           'threshold': 0.65,           'add_to_milestone': True,           'sift': True,           'is_image_cut': True,           'filename': 'tuijianhengtiao2.png'         }"
    whole = 'python /Users/jayce/Jayce-iOSPerformance/NewsPerformance/newsreaderAuto2/core/get_time.py  --scene list_refresh --path %s  --methods "%s" "%s"' %(path,half1,half2)
    os.system('python /Users/jayce/Jayce-iOSPerformance/NewsPerformance/newsreaderAuto2/core/get_time.py --scene list_refresh --path %s  --methods "%s" "%s" ' %(path,half1,half2))
    print whole

launch = Process(target=Launch)
launch.start()
launch.join()

list = []
for x in xrange(0,10):
    time_now = int(time.time())
    LaunchPath = time_now
    mkpath ="/Users/jayce/PerformanceOutput/NetEase/Refresh-toutiao/%s" %(time_now)
    list.append(mkpath)
    a = Process(target=run_Record)
    b = Process(target=run_proc)
    #c = Process(target=fenzhen)
    a.start()
    b.start()
    b.join()
    a.join()
    #c.start()

LaunchPath = list
end = Process(target=EndApp)
end.start()
end.join()
print 'last'

for x in xrange(0,10):
    path = LaunchPath[x]
    cur_path =path
    os.chdir(cur_path)
    print path
    fenzhen(path)
    pass

for x in xrange(0,10):
    path = LaunchPath[x]
    a = Process(target= CV(path))
    #a.start()
    #a.join()
    pass