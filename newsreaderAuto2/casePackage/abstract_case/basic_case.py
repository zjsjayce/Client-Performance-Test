#!/usr/bin/python
# coding= utf-8
import os

import Utils.logger as logger
import case
import casePackage.utils.adb_shell_cmd as adb_shell_cmd
import casePackage.utils.constants as constants


LOGGING = logger.get_logger(__name__)


class Case(case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device)
        self.category = constants.BASIC_RESULT_DIR
        self.batch_num = batch_num
        self.zip_file_name = self.batch_num + "_" + self.category + "_" + self.branch + "_" + self.buildId + "_" + self.device \
                             + "_" + self.app + "_" + self.getUploadScene().value + "_" + self.create_date_str.replace("-", "").replace(":", "").replace(" ", "-") + ".zip"
        self.zip_file_path = os.path.join(constants.AUTO_PATH, "uploads", self.zip_file_name)
        self.result_leaf_dir = os.path.join(self.result_root_dir, self.category, self.device +
                                       "_" + self.app + "_" + self.getUploadScene().value + "_" +
                                           self.create_date_str.replace("-", "").replace(":", "").replace(" ", "_"))
        if not os.path.exists(os.path.join(constants.AUTO_PATH, "uploads")):
            os.makedirs(os.path.join(constants.AUTO_PATH, "uploads"))
        if not os.path.exists(self.result_leaf_dir):
            os.makedirs(self.result_leaf_dir)
        self.log_tag = '[' + self.batch_num + ']: ' + '[' + device + ']' + ': result_leaf_dir' + \
                       str(self.result_leaf_dir).split('\\')[-1]
        self.csv_file_name = self.app + "_" + self.app_version + "_" + self.getUploadScene().value + "_" + self.create_date_str.replace(
            "-",
            "").replace(
            ":", "").replace(" ", "") + ".csv"
        self.log_tag = '[' + self.batch_num + ']: ' + '[' + device + ']' + ': result_leaf_dir' + \
                       str(self.result_leaf_dir).split('\\')[-1]

    def collect_csv(self, sourcePath):
        adb_shell_cmd.pullFile(self.device, sourcePath, self.result_leaf_dir)

    def after_case_exec(self):
        LOGGING.info("in basic_case after_case_exec")
        self.collect_csv(constants.emmagee_dir + self.csv_file_name)
        super(Case, self).after_case_exec()
