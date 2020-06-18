#!/usr/bin/python
# coding= utf-8

import os
import sys
import time
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "..")))
import Utils.logger as logger
import casePackage.abstract_case.basic_case as basic_case
import casePackage.utils.apptool as apptool
import casePackage.utils.constants as constants
import casePackage.utils.adb_shell_cmd as adb_shell_cmd


app = apptool.NETEASE
scene = 'netease_list_refresh_basic'

LOGGING = logger.get_logger(__name__)

class Case(basic_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        basic_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def case(self):
        self.apptools.pmClearApp()
        time.sleep(2)
        adb_shell_cmd.startApp(self.device, self.app)
        time.sleep(10)
        adb_shell_cmd.prepareEmmageeService(self.device)
        adb_shell_cmd.stopEmmageeService(self.device)  # stop first
        adb_shell_cmd.startEmmageeService(self.device, constants.package.get(app), self.csv_file_name)
        self.do_refresh()
        adb_shell_cmd.stopEmmageeService(self.device)
        self.after_case_exec()

    def do_refresh(self):
        start_timeStamp = current_timeStamp = int(time.time())
        i = 1;
        while current_timeStamp - start_timeStamp < constants.TEST_DURATION:
            element = self.m.find_element("//android.widget.LinearLayout/android.widget.TextView[@text='首页']")
            if not element:
                LOGGING.error("didn't find 首页 in do_refresh")
                break
            element.click()
            LOGGING.info("refresh for " + str(i) + "times")
            i += 1
            time.sleep(20)
            current_timeStamp = int(time.time())

if __name__ == "__main__":
    case = Case(app, scene)
    case.case()