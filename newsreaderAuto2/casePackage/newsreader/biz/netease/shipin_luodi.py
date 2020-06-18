#!/usr/bin/python
# coding= utf-8
"""
视频详情页
"""
import time

from casePackage.abstract_case import biz_case as biz_case
import Utils.exception as exception
import casePackage.utils.constants as constants
import casePackage.utils.apptool as apptool

app = apptool.NETEASE
scene = 'shipin_luodi'

class Case(biz_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        biz_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def enter_shipin(self):
        count = 0
        while True:
            element = self.m.netease_find_shipin_tab()
            if element:
                element.click()
                return True
            self.apptools.swipe(0.8, 0.12, 0.2, 0.12)
            count += 1
            if count > 20:
                return False

    def case(self):
        # self.apptools.pmClearApp()
        self.before_case_exec()
        self.apptools.forceStopApp()
        self.apptools.start()
        time.sleep(7)
        isEnter = self.enter_shipin()
        if not isEnter:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find 视频 tab in netease_shipin_luodi",
                                         RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        # refresh the list
        self.apptools.swipe(0.5, 0.3, 0.5, 0.6)
        time.sleep(3)

        for i in range(0, 10):
            video_item = self.m.netease_find_video_item()
            if video_item:
                break
        if not video_item:
            raise exception.CaseExecutingException(self.log_tag + "Didn't find shipin_item in netease_shipin_luodi",
                                                   RuntimeError(constants.FIND_FAIL_EXCE_MSG))
        self.startRecord(8)
        time.sleep(1)
        self.apptools.click_at(video_item.x - 200, video_item.y)
        time.sleep(8)
        self.listener.stop()
        tmp_save = self.saveRecord()
        # self.gt.image_path = tmp_save
        # self.gt.start()
        # self.gt.join()
        # self.after_case_exec()


if __name__ == "__main__":
    case = Case(app, scene)
    case.case()