#!/usr/bin/python
# coding= utf-8
"""
推荐列表页,视频类新闻,落地页起播时间
"""
import os
import sys
import time

import casePackage.utils.constants as constants
import Utils.exception as exception

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from casePackage.abstract_case import biz_case as biz_case
import casePackage.utils.apptool as apptool

app = apptool.BAIDU
scene = 'baidu_tuwen'

class Case(biz_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device=None):
        biz_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device)

    def case(self):
        # self.apptools.pmClearApp()
        self.apptools.start()
        time.sleep(5)
        self.apptools.swipe(0.5, 0.3, 0.5, 0.6)
        time.sleep(3)
        tuwen_item = self.m.toutiao_find_tuwen_item()
        if not tuwen_item:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find tuwen_item tab in toutiao_tuji",
                                                   RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        self.point(tuwen_item)
        self.after_case_exec()


if __name__ == "__main__":
    case = Case(app, scene)
    case.case()