#!/usr/bin/python
# coding= utf-8

import abc
import datetime
import sys
import os
import time

from runner import Runner

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "..")))
import Utils.logger as logger
import casePackage.otherThread.env as env

import casePackage.utils.apptool as apptool
import casePackage.utils.constants as constants
import casePackage.utils.tools as tools
from casePackage.utils.module import module as module
import casePackage.utils.config_reader as config_reader

LOGGING = logger.get_logger(__name__)

class Case(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device):
        if not device:
            self.listener, self.driver = env.getDriver(app)
            self.device = env.getConfig().get('init', 'deviceName')
        else:
            self.device = device
            self.listener, self.driver = env.getDriver(app, device=self.device)
        self.app = app
        self.scene = scene
        self.buildId = buildId
        self.branch = branch
        self.app_version = app_version
        self.batch_num = batch_num
        self.category = "not_set"
        self.zip_file_name = "not_set"
        self.zip_file_path = "not_set"
        # self.create_date_str = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        self.create_date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.root_dir = os.path.join(os.path.join(constants.AUTO_PATH, self.device))
        self.result_root_dir = os.path.join(self.root_dir, constants.ROOT_RESULT_DIR)
        self.apptools = apptool.apptool(self.app, self.device, self.scene)
        self.m = module(self.driver, self.app, self.apptools, self.batch_num)
        self.cv_config = config_reader.read(self.device)

    @abc.abstractmethod
    def case(self):
        pass

    def result_upload(self):
        tools.generateZip(self.result_leaf_dir, self.zip_file_path)
        if Runner.upload:
            file = {'file': open(self.zip_file_path, 'rb')}
            values = {'type': self.category, 'buildId': self.buildId}
            response = tools.uploadFile(constants.UPLOAD_FILE_URL, file, values)
            LOGGING.info(self.log_tag + "response status:" + str(response.status_code))
            LOGGING.info(self.log_tag + "response text:" + response.text)


    def before_case_exec(self):
        pass


    def after_case_exec(self):
        LOGGING.info("in casePackage after_case_exec")
        self.result_upload()

    def getUploadScene(self):
        # Caution! 必须先用==严格比较SCENE.COLDSTART_NOAD和SCENE.COLDSTART_AD的情况，否则SCENE.COLDSTART_NOAD，
        # SCENE.COLDSTART_AD都会命中 "coldstart" in str(self.scene)
        if self.scene == constants.SCENE.COLDSTART_NOAD:
            return constants.SCENE.COLDSTART_NOAD
        elif self.scene == constants.SCENE.COLDSTART_AD:
            return constants.SCENE.COLDSTART_AD

        if self.scene == constants.SCENE.HOTSTART_AD:
            return constants.SCENE.HOTSTART_AD
        elif self.scene == constants.SCENE.HOTSTART_NOAD:
            return constants.SCENE.HOTSTART_NOAD

        if self.scene == constants.SCENE.COLDSTART_NEWUSER__NOAD:
            return constants.SCENE.COLDSTART_NEWUSER__NOAD
        elif self.scene == constants.SCENE.COLDSTART_NEWUSER_AD:
            return constants.SCENE.COLDSTART_NEWUSER_AD

        # after SCENE.COLDSTART_NOAD and SCENE.COLDSTART_AD, do the rest compare
        elif "newuser" in str(self.scene):
            return constants.SCENE.COLDSTART_NEWUSER
        elif "coldstart" in str(self.scene):
            return constants.SCENE.COLDSTART
        elif "hotstart" in str(self.scene):
            return constants.SCENE.HOTSTART
        elif "list_refresh" in str(self.scene):
            return constants.SCENE.LIST_REFRESH
        elif "shipin_luodi" in str(self.scene):
            return constants.SCENE.SHIPIN_LUODI
        elif "tuji" in str(self.scene):
            return constants.SCENE.TUJI
        elif "tuwen" in str(self.scene):
            return constants.SCENE.TUWEN
        elif "shipin_shouzhen" in str(self.scene):
            return constants.SCENE.SHIPIN_SHOUZHEN


