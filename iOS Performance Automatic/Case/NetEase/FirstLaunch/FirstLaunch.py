# -*- encoding=utf8 -*-
__author__ = "jayce"

from airtest.core.api import *
import threading
from multiprocessing import Process
import os
import time
import numpy as np

os.system('python -m airtest run /Users/jayce/Jayce-iOSPerformance/Case/NetEase/FirstLaunch/FirstLaunch.air  --device iOS:///127.0.0.1:8100 --log  /Users/jayce/Desktop/Airtest')