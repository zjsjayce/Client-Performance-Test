#!/usr/bin/python
# coding= utf-8
"""
腾讯新闻图集详情页加载
"""
import os
import sys
import time

import casePackage.utils.constants as constants
import Utils.exception as exception

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from casePackage.abstract_case import biz_case as biz_case
import casePackage.utils.apptool as apptool

app = apptool.TENCENT
scene = 'tuji'

class Case(biz_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        biz_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def enter_tuji(self):
        count = 0
        while True:
            element = self.m.tencent_find_tuji_tab()
            if element and element.x < self.apptools.window_size()[0] - 50:
                element.click()
                return True
            self.apptools.swipe(0.8, 0.12, 0.2, 0.12)
            count += 1
            if count > 20:
                return False

    def case(self):
        print 'a'
        # self.apptools.pmClearApp()
        self.apptools.forceStopApp()
        self.apptools.start()
        time.sleep(8)
        isEnter = self.enter_tuji()
        if not isEnter:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find 图片 tab in toutiao_tuji",
                                                   RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        self.apptools.swipe(0.5, 0.3, 0.5, 0.6)
        time.sleep(2)

        tuji_item = self.m.tencent_find_tuji_item()
        if not tuji_item:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find tuji_item tab in toutiao_tuji",
                                                   RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        self.point(tuji_item)
        self.after_case_exec()


if __name__ == "__main__":
    case = Case(app, scene)
    case.case()