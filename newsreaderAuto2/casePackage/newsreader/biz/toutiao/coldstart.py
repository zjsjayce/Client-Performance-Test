#!/usr/bin/python
# coding= utf-8

import os
import sys
import time
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from casePackage.abstract_case import biz_case as biz_case
import casePackage.utils.apptool as apptool
import casePackage.utils.constants as constants
from casePackage.utils import tools

app = apptool.TOUTIAO
scene = 'coldstart'

class Case(biz_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        biz_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def case(self):
        self.before_case_exec()
        self.apptools.forceStopApp()
        time.sleep(2)
        self.startRecord(10)
        time.sleep(1)
        self.apptools.startApp()
        time.sleep(10)
        self.listener.stop()
        self.saveRecord()
        # self.dealAds()
        # self.after_case_exec()

    # def dealAds(self):
    #     # templateFilePath = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")),
    #     #              'res/' + 'netease_ad_bottom.png')
    #     # tem = Template(templateFilePath)
    #     # jpgs = filter(lambda fileName: 'jpg' in fileName, os.listdir(self.result_leaf_dir))
    #     # jpgs.sort()
    #     # if tem.match_in(os.path.join((self.result_leaf_dir), jpgs[4])):
    #     #     self.scene = constants.SCENE.COLDSTART_AD
    #     # else:
    #     #     self.scene = constants.SCENE.COLDSTART_NOAD
    #     jpgs = filter(lambda fileName: 'jpg' in fileName, os.listdir(self.result_leaf_dir))
    #     jpgs.sort()
    #     if self.gt._is_white_screen(os.path.join(self.tmp_save_path, jpgs[4]), num=0.5):
    #         self.scene = constants.SCENE.COLDSTART_NOAD
    #     else:
    #         self.scene = constants.SCENE.COLDSTART_AD
    #     new_result_leaf_dir = os.path.join(self.result_root_dir, self.category, self.device +
    #                                    "_" + self.app + "_" + self.app_version + "_" + self.getUploadScene().value + "_" +
    #                                        self.create_date_str.replace("-", "").replace(":", "").replace(" ", "_"))
    #     if not os.path.exists(new_result_leaf_dir):
    #         os.makedirs(new_result_leaf_dir)
    #     for file in os.listdir(self.result_leaf_dir):
    #         shutil.move(os.path.join(self.result_leaf_dir, file), os.path.join(new_result_leaf_dir, file))
    #     shutil.rmtree(self.result_leaf_dir)
    #     self.result_leaf_dir = new_result_leaf_dir
    #     self.zip_file_name = self.batch_num + "_" + self.category + "_" + self.buildId + "_" + self.device \
    #                          + "_" + self.app + "_" + self.scene.value + "_" + self.create_date_str.replace("-",
    #                                                                                                              "").replace(
    #         ":", "").replace(" ", "-") + ".zip"
    #     self.zip_file_path = os.path.join(constants.AUTO_PATH, "uploads", self.zip_file_name)
