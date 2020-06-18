#!/usr/bin/python
# coding= utf-8

import os
import sys
import time

import Utils.logger as logger
from casePackage.abstract_case import basic_case as basic_case
import casePackage.utils.apptool as apptool
import casePackage.utils.constants as constants
import casePackage.utils.adb_shell_cmd as adb_shell_cmd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = apptool.NETEASE
scene = 'netease_shipin_shouzhen_basic'
loop = 5

LOGGING = logger.get_logger(__name__)

class Case(basic_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device=None):
        basic_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device)

    def case(self):
        self.apptools.pmClearApp()
        time.sleep(2)
        self.apptools.start()
        time.sleep(10)
        adb_shell_cmd.prepareEmmageeService(self.device)
        adb_shell_cmd.stopEmmageeService(self.device)  # stop first
        adb_shell_cmd.startEmmageeService(self.device, constants.package.get(app), self.csv_file_name)
        self.do_shipin_shouzhen(loop)
        time.sleep(20)
        adb_shell_cmd.stopEmmageeService(self.device)
        self.after_case_exec()

    def do_shipin_shouzhen(self, loop):
        self.enter_shipin()
        i = 0
        while i < loop:
            video_item = self.m.netease_find_video_start()
            if video_item:
                self.apptools.click_at(video_item.x, video_item.y)
                i += 1
                time.sleep(3)
            self.apptools.swipe(0.5, 0.7, 0.5, 0.3)

    def enter_shipin(self):
        count = 0
        while True:
            element = self.m.netease_find_shipin_tab()
            if element:
                element.click()
                return True
            self.apptools.swipe(0.8, 0.12, 0.2, 0.12)
            count += 1
            if count > 20:
                return False

if __name__ == "__main__":
    case = Case(app, scene, "", "grey", "46.1")
    case.case()