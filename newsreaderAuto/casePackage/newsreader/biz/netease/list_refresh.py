#!/usr/bin/python
# coding= utf-8
"""
头条列表刷新
"""
import time

import casePackage.utils.constants as constants
from casePackage.abstract_case import biz_case as biz_case
import casePackage.utils.apptool as apptool
import Utils.logger as logger
import Utils.exception as exception

app = apptool.NETEASE
scene = 'list_refresh'

LOGGING = logger.get_logger(__name__)
class Case(biz_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        biz_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def case(self):
        self.before_case_exec()
        self.apptools.forceStopApp()
        self.apptools.start()
        time.sleep(7)
        element = self.m.find_element("//android.widget.LinearLayout/android.widget.TextView[@text='首页']")
        if not element:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find 首页 in list_refresh", RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        self.startRecord(7)
        time.sleep(1)
        element.click()
        time.sleep(7)
        self.listener.stop()
        tmp_save = self.saveRecord()
        # self.gt.image_path = tmp_save
        # self.gt.start()
        # self.gt.join()
        # self.after_case_exec()


if __name__ == "__main__":
    case = Case(app, scene)
    case.case()