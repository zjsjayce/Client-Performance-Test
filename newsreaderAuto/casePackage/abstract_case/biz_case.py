#!/usr/bin/python
# coding= utf-8
import os
import shutil
import sys
import time

import Utils.logger as logger
import Utils.exception as exception
from casePackage.abstract_case import case as case
import casePackage.utils.constants as constants
import casePackage.utils.adb_shell_cmd as adb_shell_cmd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "..")))

LOGGING = logger.get_logger(__name__)


class Case(case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device)
        self.category = constants.BIZ_RESULT_DIR
        self.batch_num = batch_num
        self.ran = ran
        self.suite = suite
        self.tmp_save_path = os.path.join(self.root_dir, self.scene)
        self.result_leaf_dir = os.path.join(self.result_root_dir, self.category, self.device +
                                       "_" + self.app + "_" + self.app_version + "_" + self.getUploadScene().value + "_" +
                                           self.create_date_str.replace("-", "").replace(":", "").replace(" ", "_"))
        if not os.path.exists(self.tmp_save_path):
            os.makedirs(self.tmp_save_path)


        if not os.path.exists(self.result_leaf_dir):
            os.makedirs(self.result_leaf_dir)

        self.log_tag = '[' + self.batch_num + ']: ' + '[' + device + ']' + ': result_leaf_dir' + str(self.result_leaf_dir).split('\\')[-1]
        self.test_file_name = self.create_date_str.replace(":", "").replace(" ", "").replace("-", "") + '.log'
        self.test_file_path = os.path.join(self.tmp_save_path, self.test_file_name)
        # self.test_file = open(os.path.join(self.tmp_save_path, self.test_file_name), 'w')
        # 201811012112_category_buildId_deviceId_app_scene_timestamp.zip
        self.zip_file_name = self.batch_num + "_" + self.category + "_" + self.buildId + "_" + self.device \
                             + "_" + self.app + "_" + self.getUploadScene().value + "_" + self.create_date_str.replace("-", "").replace(":", "").replace(" ", "-") + ".zip"
        self.zip_file_path = os.path.join(constants.AUTO_PATH, "uploads", self.zip_file_name)
        if not os.path.exists(os.path.join(constants.AUTO_PATH, "uploads")):
            os.makedirs(os.path.join(constants.AUTO_PATH, "uploads"))
        # self.gt = Get_time(self.suite, self.ran, self.batch_num, self.device, self.scene, self.test_file_path, self.tmp_save_path, self.result_leaf_dir,
        #                    self.cv_config.get(self.app).get(self.scene).get('method_dicts'))
        self.clear_tmp_dir()


    def before_case_exec(self):
        self.log_case_info()


    def after_case_exec(self):
        # self.log_case_info()
        super(Case, self).after_case_exec()

    def log_case_info(self):
        self.test_file_path = os.path.join(self.tmp_save_path, self.test_file_name)
        self.test_file = open(self.test_file_path, 'a')
        self.log("createDate: " + self.create_date_str)
        self.log("buildId: " + self.buildId)
        self.log("branch: " + self.branch)
        self.log("system: android")
        self.log("deviceId: " + self.apptools.device)
        self.log("deviceBrand: " + self.apptools.get_brand())
        self.log("deviceModel: " + self.apptools.get_model())
        self.log("systemVersion: " + self.apptools.get_android_version())
        self.log("romName: " + self.apptools.get_rom_name())
        self.log("romVersion: " + self.apptools.get_rom_version())
        self.log("appName: " + self.app)
        self.log("appVersion: " + adb_shell_cmd.get_app_version(self.device, constants.package.get(self.app)))
        # self.log("scene: " + self.getUploadScene().value)
        self.test_file.flush()
        self.test_file.close()

    def log(self, content):
        self.test_file.write(content + '\n')

    def clear_tmp_dir(self):
        cur_path = os.getcwd()
        os.chdir(self.tmp_save_path)
        os.system('del *.log')
        os.system('del *.jpg')
        os.system('del *.mp4')
        os.chdir(cur_path)

    def startRecord(self, duration):
        bSuccess = self.m.getVideo(duration)
        if not bSuccess:
            raise exception.CaseExecutingException(self.log_tag,
                                                   RuntimeError(constants.RECORD_FAIL_EXCE_MSG))

    def saveRecord(self):
        tmp_save = self.m.saveVideo()
        video_abs_path = os.path.join(tmp_save, 'video.mp4')
        if not os.path.exists(video_abs_path):
            raise exception.CaseExecutingException(self.log_tag + "Video generate failed. video file does not exist.", RuntimeError(constants.RECORD_FAIL_EXCE_MSG))

        uncheckedPath = os.path.join(os.path.join(constants.AUTO_PATH, self.apptools.device), constants.ROOT_RESULT_DIR,
                                     constants.UNCHECKED, self.device + "_" + self.app + "_" + self.app_version + "_" + self.getUploadScene().value + "_" +
                                        self.create_date_str.replace("-", "").replace(":", "").replace(" ", "_"))
        shutil.copytree(tmp_save, uncheckedPath)


    def point(self, element):
        if element:
            self.startRecord(10)
            time.sleep(1)
            element.click()
            time.sleep(10)
            self.listener.stop()
            tmp_save = self.saveRecord()
            # self.gt.image_path = tmp_save
            # self.gt.start()
            # self.gt.join()