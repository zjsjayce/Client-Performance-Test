# -*- coding: utf-8 -*-
import threading
import time

from Utils import logger
from casePackage.utils import adb_shell_cmd

LOGGING = logger.get_logger(__name__)
class TimeoutMonitorThread(threading.Thread):
    def __init__(self, timeout, device):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self.isStop = False
        self.device = device


    def stop(self):
        self.isStop = True


    def run(self):
        self.startTime = time.time()
        LOGGING.info("start to monitor timeout")
        while not self.isStop:
            if time.time() - self.startTime > self.timeout:
                LOGGING.error("timeout restart adb")
                adb_shell_cmd.restart_adb(self.device)
                # sleep 控制等待appium check服务重启appium，外面会join此线程，因此下个case执行时会正常
                time.sleep(2 * 60)
                # 重置计时起点
                self.startTime = time.time()
            else:
                time.sleep(30)
        LOGGING.info("case finished, stop monitor timeout")