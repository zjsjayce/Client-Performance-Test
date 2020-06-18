#!/usr/bin/python
# coding= utf-8
"""
网易新闻冷启动时间
"""
import os
import shutil
import time

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import casePackage.utils.adb_shell_cmd as adb_shell_cmd
import casePackage.abstract_case.biz_case as biz_case
import casePackage.utils.apptool as apptool
import Utils.logger as logger
import casePackage.utils.constants as constants
from casePackage.utils import tools

app = apptool.NETEASE
scene = 'coldstart'
LOGGING = logger.get_logger(__name__)

class Case(biz_case.Case):

    def __init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite):
        biz_case.Case.__init__(self, app, scene, buildId, branch, app_version, batch_num, device, ran, suite)

    def case(self):
        self.before_case_exec()
        adb_shell_cmd.forceStopApp(self.device, self.app)
        time.sleep(2)
        self.startRecord(10)
        time.sleep(1)
        adb_shell_cmd.startApp(self.device, self.app)
        time.sleep(10)
        self.listener.stop()
        self.saveRecord()
        # self.bSuccess = self.gt.run()
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
    #     if tools.find_text("跳过", os.path.join((self.result_leaf_dir), jpgs[4])):
    #         self.scene = constants.SCENE.COLDSTART_AD
    #     else:
    #         self.scene = constants.SCENE.COLDSTART_NOAD
    #     new_result_leaf_dir = os.path.join(self.result_root_dir, self.category, self.device +
    #                                    "_" + self.app + "_" + self.getUploadScene().value + "_" +
    #                                        self.create_date_str.replace("-", "").replace(":", "").replace(" ", "_"))
    #     if not os.path.exists(new_result_leaf_dir):
    #         os.makedirs(new_result_leaf_dir)
    #     for file in os.listdir(self.result_leaf_dir):
    #         shutil.move(os.path.join(self.result_leaf_dir, file), os.path.join(new_result_leaf_dir, file))
    #     shutil.rmtree(self.result_leaf_dir)
    #     self.result_leaf_dir = new_result_leaf_dir
    #     self.zip_file_name = self.batch_num + "_" + self.category + "_" + self.buildId + "_" + self.device \
    #                          + "_" + self.app + "_" + self.app_version + "_" + self.scene.value + "_" + self.create_date_str.replace("-",
    #                                                                                                              "").replace(
    #         ":", "").replace(" ", "-") + ".zip"
    #     self.zip_file_path = os.path.join(constants.AUTO_PATH, "uploads", self.zip_file_name)


if __name__ == "__main__":
    case = Case(app, scene)
    case.case()