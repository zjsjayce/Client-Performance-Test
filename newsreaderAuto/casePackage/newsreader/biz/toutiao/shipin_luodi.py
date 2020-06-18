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

from casePackage.abstract_case import biz_case as biz_case
import casePackage.utils.apptool as apptool

app = apptool.TOUTIAO
scene = 'shipin_luodi'

class Case(biz_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        biz_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def enter_shipin(self):
        count = 0
        while True:
            element = self.m.toutiao_find_shipin_tab()
            if element:
                element.click()
                return True
            self.apptools.swipe(0.8, 0.12, 0.2, 0.12)
            count += 1
            if count > 20:
                return False

    def case(self):
        # self.apptools.pmClearApp()
        self.apptools.forceStopApp()
        self.apptools.start()
        time.sleep(15)
        isEnter = self.enter_shipin()
        if not isEnter:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find 视频 tab in toutiao_shipin_luodi",
                                                   RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        self.apptools.swipe(0.5, 0.3, 0.5, 0.6)
        time.sleep(3)

        for i in range(0, 10):
            video_item = self.m.toutiao_find_video_item()
            if video_item:
                break
        if not video_item:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find shipin_item in toutiao_shipin_luodi",
                                                   RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        self.startRecord(7)
        time.sleep(1)
        self.apptools.click_at(video_item.x - 100, video_item.y)
        time.sleep(7)
        tmp_save = self.saveRecord()
        # self.gt.image_path = tmp_save
        # self.gt.start()
        # self.gt.join()
        # self.after_case_exec()


if __name__ == "__main__":
    case = Case(app, scene)
    case.case()