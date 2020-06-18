#!/usr/bin/python
# coding= utf-8

"""
图集详情页
"""
import os
import time

import casePackage.utils.constants as constants
import Utils.exception as exception

from casePackage.abstract_case import biz_case as biz_case
import casePackage.utils.apptool as apptool

app = apptool.NETEASE
scene = 'tuji'

class Case(biz_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        biz_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

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

    def case(self):
        self.before_case_exec()
        self.apptools.pmClearApp()
        self.apptools.start()
        time.sleep(7)
        isEnter = self.enter_tuji()
        if not isEnter:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find 图片 tab in netease_tuji",
                                                   RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        time.sleep(1)
        tuji_item = self.m.netease_find_tuji_item()
        if not tuji_item:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find tuji_item in netease_tuji",
                                                   RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        self.point(tuji_item)
        # self.after_case_exec()


if __name__ == "__main__":
    case = Case(app, scene)
    case.case()