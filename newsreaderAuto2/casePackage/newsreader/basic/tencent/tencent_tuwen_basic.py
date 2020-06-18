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

app = apptool.TENCENT
scene = 'tencent_tuwen_basic'

LOGGING = logger.get_logger(__name__)

class Case(basic_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        basic_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def case(self):
        self.apptools.pmClearApp()
        time.sleep(2)
        self.apptools.start()
        # take more seconds to click out permission
        time.sleep(15)
        adb_shell_cmd.prepareEmmageeService(self.device)
        adb_shell_cmd.stopEmmageeService(self.device)  # stop first
        adb_shell_cmd.startEmmageeService(self.device, constants.package.get(app), self.csv_file_name)
        self.do_tuwen()
        time.sleep(20)
        adb_shell_cmd.stopEmmageeService(self.device)
        self.after_case_exec()

    def do_tuwen(self):
        LOGGING.info("start do_tuwen")
        start_timeStamp = current_timeStamp = int(time.time())
        test_times = 1
        while current_timeStamp - start_timeStamp < constants.TEST_DURATION:
            textView_element = self.m.tencent_find_tuwen_item()
            if not textView_element:
                LOGGING.error("didn't find tuwen item in do_tuwen")
                break
            else:
                textView_element.click()
            LOGGING.info("refresh for " + str(test_times) + "times")
            test_times += 1
            time.sleep(20)
            adb_shell_cmd.press_back(self.device)
            current_timeStamp = int(time.time())

if __name__ == "__main__":
    case = Case(app, scene, "", "grey", "46.1")
    case.case()