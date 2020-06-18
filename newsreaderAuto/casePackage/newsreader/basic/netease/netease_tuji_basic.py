#!/usr/bin/python
# coding= utf-8

import os
import sys
import time

import Utils.logger as logger
import casePackage.abstract_case.basic_case as basic_case
import casePackage.utils.apptool as apptool
import casePackage.utils.constants as constants
import casePackage.utils.adb_shell_cmd as adb_shell_cmd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = apptool.NETEASE
scene = 'netease_tuji_basic'
loop = 3

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
        self.do_tuji(loop)
        time.sleep(20)
        adb_shell_cmd.stopEmmageeService(self.device)
        self.after_case_exec()

    def do_tuji(self, loop):
        self.enter_tuji()
        i = 0
        while i < loop:
            tuji_item = self.m.netease_find_tuji_item()
            if tuji_item:
                self.apptools.click_at(tuji_item.x, tuji_item.y)
                i += 1
                time.sleep(3)
                adb_shell_cmd.input_keyevent(self.device, constants.KEYCODE_BACk)
            self.apptools.swipe(0.5, 0.7, 0.5, 0.3)

    def enter_tuji(self):
        count = 0
        while True:
            element = self.m.netease_find_tuji_tab()
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