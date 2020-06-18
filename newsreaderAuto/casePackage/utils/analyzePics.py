#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import threading
import time

from Utils.logger import get_logger
from casePackage.utils import constants, config_reader, tools, apptool
from core.get_time import Get_time

LOGGING = get_logger(__name__)


class AnalyzePics(threading.Thread):
    def __init__(self, suite, category, device, ran, batch_num, buildId, upload):
        threading.Thread.__init__(self)
        self.device = device
        self.category = category[0].value
        self.stopped = False
        self.suite = suite
        self.ran = ran
        self.batch_num = batch_num
        self.buildId = buildId
        self.upload = upload
        self.result_root_dir = os.path.join(constants.AUTO_PATH, self.device, constants.ROOT_RESULT_DIR)
        self.uncheckedRoot = os.path.join(self.result_root_dir, constants.UNCHECKED)


    def stop(self):
        self.stopped = True


    def result_upload(self, result_leaf_dir, zip_file_path):
        tools.generateZip(result_leaf_dir, zip_file_path)
        if self.upload:
            file = {'file': open(zip_file_path, 'rb')}
            values = {'type': self.category, 'buildId': self.buildId}
            response = tools.uploadFile(constants.UPLOAD_FILE_URL, file, values)
            log_tag = '[' + self.batch_num + ']: ' + '[' + self.device + ']' + ': result_leaf_dir' + \
                           str(result_leaf_dir).split('\\')[-1]
            LOGGING.info(log_tag + "response status:" + str(response.status_code))
            LOGGING.info(log_tag + "response text:" + response.text)


    def run(self):
        while not self.stopped:
            try:
                self.checkUnchecked()
                time.sleep(5)
            except Exception:
                LOGGING.exception("exception caught in analyzePics thread")
        self.checkUnchecked()
        LOGGING.info("analyze thread stopped" + self.suite + '-' + self.batch_num)



    def checkUnchecked(self):
            uncheckedDirs = os.walk(self.uncheckedRoot)
            for path, dir_list, _ in uncheckedDirs:
                for dir_name in dir_list:
                    sections = dir_name.split('_')
                    oneAnalyze = OneAnalyze(self.suite, self.ran, self.batch_num, self.buildId, self.device
                                            , self.category, sections[1], sections[2], sections[3],
                                            sections[4] + '_' + sections[5], os.path.join(path, dir_name),
                                            self.result_root_dir)
                    try:
                        oneAnalyze.gt.run()
                        time.sleep(1)
                        shutil.rmtree(oneAnalyze.to_analyze)

                        if 'start' in oneAnalyze.scene:
                            oneAnalyze.dealAds()
                        oneAnalyze.addSceneInfoInLog()

                    except Exception:
                        LOGGING.exception(self.suite + '-' + self.batch_num + "exception in checkUnchecked")
                        shutil.rmtree(oneAnalyze.to_analyze)

                    zip_file_name = self.batch_num + "_" + self.category + "_" + self.buildId + "_" + self.device \
                                    + "_" + oneAnalyze.app + "_" + constants.getUploadScene(
                        oneAnalyze.scene).value + "_" + oneAnalyze.create_date_str.replace("_", "-") + ".zip"
                    self.result_upload(oneAnalyze.result_leaf_dir, os.path.join(constants.AUTO_PATH, "uploads", zip_file_name))


def getCaseName(app, scene):
     if app == apptool.NETEASE:
        if 'refresh' in scene:
            return 'list_refresh'
        if 'tuji' in scene:
            return 'tuji'
        if 'shipin-luodi' in scene:
            return 'shipin_luodi'
        if 'shipin-shouzhen' in scene:
            return 'shipin_shouzhen'
        if 'tuwen' in scene:
            return 'tuwen'
        if 'newuser' in scene:
            return 'coldstart_newuser'
        else:
            return scene
     if app == apptool.TOUTIAO:
        if 'hotstart' in scene:
             return 'hotstart'
        if 'coldstart' in scene:
            return 'coldstart'
        if 'refresh' in scene:
            return 'list_refresh'
        if 'tuji' in scene:
            return 'tuji'
        if 'shipin-luodi' in scene:
            return 'shipin_luodi'
        if 'shipin-shouzhen' in scene:
            return 'shipin_shouzhen'
        if 'tuwen' in scene:
            return 'tuwen'
        else:
            return scene

     if app == apptool.TENCENT:
        if 'hotstart' in scene:
            return 'hotstart'
        if 'coldstart' in scene:
            return 'coldstart'
        if 'refresh' in scene:
            return 'list_refresh'
        if 'tuji' in scene:
            return 'tuji'
        if 'shipin-luodi' in scene:
            return 'shipin_luodi'
        if 'shipin-shouzhen' in scene:
            return 'shipin_shouzhen'
        if 'tuwen' in scene:
            return 'tuwen'
        else:
            return scene

class OneAnalyze(object):
    def __init__(self, suite, ran, batch_num, buildId, device, category, app, appVersion, scene, create_date_str, to_analyze, result_root_dir):
        self.suite = suite
        self.ran = ran
        self.batch_num = batch_num
        self.buildId = buildId
        self.device = device
        self.cv_config = config_reader.read(self.device)
        self.category = category
        self.app = app
        self.appVersion = appVersion
        self.scene = getCaseName(self.app, scene)
        self.create_date_str = create_date_str
        self.to_analyze = to_analyze
        self.result_root_dir = result_root_dir
        self.test_file_name = self.create_date_str.replace('_', "") + '.log'
        self.result_leaf_dir = os.path.join(self.result_root_dir, self.category, self.device +
                                       "_" + app + "_" + self.appVersion + "_" + constants.getUploadScene(
            self.scene).value + "_" + self.create_date_str)
        self.test_file_path = os.path.join(self.to_analyze, self.test_file_name)

        self.gt = Get_time(self.suite, self.ran, self.batch_num, self.device, self.scene, self.test_file_path, self.to_analyze, self.result_leaf_dir,
                           self.cv_config.get(self.app).get(self.scene).get('method_dicts'))

    def dealAds(self):
        jpgs = filter(lambda fileName: 'jpg' in fileName, os.listdir(self.result_leaf_dir))
        jpgs.sort()
        if self.gt._is_white_screen(os.path.join(self.result_leaf_dir, jpgs[4]), num=0.5):
            if self.scene.__contains__("hotstart"):
                self.scene = constants.SCENE.HOTSTART_NOAD
            elif self.scene.__contains__("newuser"):
                self.scene = constants.SCENE.COLDSTART_NEWUSER__NOAD
            else:
                self.scene = constants.SCENE.COLDSTART_NOAD
        else:
            if self.scene.__contains__("hotstart"):
                self.scene = constants.SCENE.HOTSTART_AD
            elif self.scene.__contains__("newuser"):
                self.scene = constants.SCENE.COLDSTART_NEWUSER_AD
            else:
                self.scene = constants.SCENE.COLDSTART_AD
        new_result_leaf_dir = os.path.join(self.result_root_dir, self.category, self.device +
                                           "_" + self.app + "_" + self.appVersion + "_" + constants.getUploadScene(self.scene).value + "_" +
                                           self.create_date_str)
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

    def addSceneInfoInLog(self):
        self.test_file = open(os.path.join(self.result_leaf_dir, self.test_file_name), 'a')
        self.test_file.write("scene: " + constants.getUploadScene(self.scene).value + '\n')
        self.test_file.flush()
        self.test_file.close()

if __name__ == "__main__":
    a = config_reader.read('573a521e')
    b = a.get('netease')
    c = a.get('netease').keys()[0]
    d = b[c].get('method_dicts')
    print d
