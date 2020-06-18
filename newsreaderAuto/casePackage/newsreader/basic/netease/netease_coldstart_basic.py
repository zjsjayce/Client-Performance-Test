#!/usr/bin/python
# coding= utf-8

import time
import Utils.logger as logger
import casePackage.abstract_case.basic_case as basic_case
import casePackage.utils.apptool as apptool
import casePackage.utils.constants as constants
import casePackage.utils.adb_shell_cmd as adb_shell_cmd


app = apptool.NETEASE
scene = 'netease_coldstart_basic'
loop = 5

LOGGING = logger.get_logger(__name__)

class Case(basic_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        basic_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def case(self):
        self.apptools.pmClearApp()
        time.sleep(2)
        adb_shell_cmd.startApp(self.device, self.app)
        self.apptools.forceStopApp()
        time.sleep(1)
        adb_shell_cmd.prepareEmmageeService(self.device)
        adb_shell_cmd.stopEmmageeService(self.device)         # stop first
        adb_shell_cmd.startEmmageeService(self.device, constants.package.get(app), self.csv_file_name)
        self.do_coldstart(10)
        adb_shell_cmd.prepareEmmageeService(self.device)
        adb_shell_cmd.stopEmmageeService(self.device)
        self.after_case_exec()

    def do_coldstart(self, loop):
        i = 0
        time.sleep(5)
        while i < loop:
            self.apptools.forceStopApp()        # 后面必须不能紧跟stopEmmagee，否则Emmagee会ANR
            i += 1
            LOGGING.info("start app: " + str(i))
            self.apptools.startApp()
            time.sleep(15)


if __name__ == "__main__":
    case = Case(app, scene)
    case.case()