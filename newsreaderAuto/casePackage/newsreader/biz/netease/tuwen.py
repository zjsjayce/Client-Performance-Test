#!/usr/bin/python
# coding= utf-8
"""
图文详情页
"""
import os
import sys
import time

import Utils.logger as logger
import casePackage.utils.constants as constants
import Utils.exception as exception

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from casePackage.abstract_case import biz_case as biz_case
import casePackage.utils.apptool as apptool

app = apptool.NETEASE
scene = 'tuwen'

LOGGING = logger.get_logger(__name__)
class Case(biz_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        biz_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def case(self):
        # self.apptools.pmClearApp()
        self.before_case_exec()
        self.apptools.forceStopApp()
        self.apptools.start()
        time.sleep(7)
        self.apptools.swipe(0.5, 0.3, 0.5, 0.6)
        time.sleep(3)
        tuwen_item = self.m.netease_find_tuwen_item()
        if not tuwen_item:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find tuwen_item in netease_tuwen",
                                                   RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        time.sleep(0.5)
        self.point(tuwen_item)
        # self.after_case_exec()

if __name__ == "__main__":
    case = Case(app, scene)
    case.case()