#!/usr/bin/python
# coding= utf-8
"""
腾讯新闻双击back退出后启动
"""
import os
import time
import shutil

import casePackage.utils.adb_shell_cmd as adb_shell_cmd
from casePackage.abstract_case import biz_case as biz_case
import casePackage.utils.apptool as apptool
import casePackage.utils.constants as constants
from casePackage.utils import tools

app = apptool.TENCENT
scene = 'hotstart'

class Case(biz_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        biz_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def case(self):
        time.sleep(7)
        adb_shell_cmd.press_back_twice(self.device)
        time.sleep(2)
        self.startRecord(7)
        time.sleep(1)
        self.apptools.startApp()
        time.sleep(7)
        tmp_save = self.saveRecord()
        # self.gt.image_path = tmp_save
        # self.gt.start()
        # self.gt.join()
        # self.dealAds()
        # self.after_case_exec()

    def dealAds(self):
        jpgs = filter(lambda fileName: 'jpg' in fileName, os.listdir(self.result_leaf_dir))
        jpgs.sort()
        if tools.find_text("跳过", os.path.join((self.result_leaf_dir), jpgs[4])):
            self.scene = constants.SCENE.HOTSTART_AD
        else:
            self.scene = constants.SCENE.HOTSTART_NOAD
        new_result_leaf_dir = os.path.join(self.result_root_dir, self.category, self.device +
                                       "_" + self.app + "_" + self.app_version + "_" + self.getUploadScene().value + "_" +
                                           self.create_date_str.replace("-", "").replace(":", "").replace(" ", "_"))
        if not os.path.exists(new_result_leaf_dir):
            os.makedirs(new_result_leaf_dir)
        for file in os.listdir(self.result_leaf_dir):
            shutil.move(os.path.join(self.result_leaf_dir, file), os.path.join(new_result_leaf_dir, file))
        shutil.rmtree(self.result_leaf_dir)
        self.result_leaf_dir = new_result_leaf_dir
        self.zip_file_name = self.batch_num + "_" + self.category + "_" + self.buildId + "_" + self.device \
                             + "_" + self.app + "_" + self.scene.value + "_" + self.create_date_str.replace("-",
                                                                                                                 "").replace(
            ":", "").replace(" ", "-") + ".zip"
        self.zip_file_path = os.path.join(constants.AUTO_PATH, "uploads", self.zip_file_name)

if __name__ == "__main__":
    case = Case(app, scene)
    case.case()