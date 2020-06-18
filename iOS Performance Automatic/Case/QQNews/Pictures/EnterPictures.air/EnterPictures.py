# -*- encoding=utf8 -*-
__author__ = "jayce"

from airtest.core.api import *
import threading
from multiprocessing import Process
import os
from poco.drivers.ios import iosPoco
import time

poco = iosPoco()
sleep(3.0)
poco("图片").click()
sleep(3.0)