#!/usr/bin/python
# coding= utf-8
"""
腾讯新闻要闻推荐列表刷新
"""
import time

import Utils.exception as exception
import casePackage.utils.constants as constants
from casePackage.abstract_case import biz_case as biz_case
import casePackage.utils.apptool as apptool

app = apptool.TENCENT
scene = 'list_refresh'

class Case(biz_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        biz_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def case(self):
        # self.m.restart_app()
        self.apptools.start()
        time.sleep(2)
        element = self.m.find_element("com.tencent.news:id/nav_tv")
        if not element:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find com.tencent.news:id/nav_tv in list_refresh_toutiao", RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        self.startRecord(7)
        time.sleep(1)
        element.click()
        time.sleep(7)
        tmp_save = self.saveRecord()
        # self.gt.image_path = tmp_save
        # self.gt.start()
        # self.gt.join()
        # self.after_case_exec()


if __name__ == "__main__":
    case = Case(app, scene)
    case.case()