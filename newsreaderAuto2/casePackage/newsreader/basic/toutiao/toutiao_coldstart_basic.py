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

app = apptool.TOUTIAO
scene = 'coldstart'
loop = 5

LOGGING = logger.get_logger(__name__)

class Case(basic_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device=None):
        basic_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device)

    def case(self):
        self.apptools.forceStopApp()
        time.sleep(2)
        adb_shell_cmd.stopEmmageeService(self.device)  # stop first
        adb_shell_cmd.startEmmageeService(self.device, constants.package.get(app), self.csv_file_name)
        self.do_coldstart(loop)
        adb_shell_cmd.stopEmmageeService(self.device)
        # self.collect_csv(constants.emmagee_dir + self.csv_file_name)
        self.after_case_exec()

    def do_coldstart(self, loop):
        i = 0
        while i < loop:
            i += 1
            self.apptools.startApp()
            time.sleep(10)
            self.apptools.forceStopApp()

if __name__ == "__main__":
    case = Case(app, scene)
    case.case()