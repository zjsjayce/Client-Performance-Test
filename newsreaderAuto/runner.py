# -*- coding: utf-8 -*-
import argparse
import datetime
import os

import configparser
import importlib
import numpy as np
import pandas as pd

import Utils.logger as logger
import requests

from casePackage.otherThread import timeoutMonitor
from casePackage.utils import adb_shell_cmd, constants, boxplot

from casePackage.utils.adb_shell_cmd import check_installed_version
from casePackage.utils.analyzePics import AnalyzePics
from casePackage.utils.constants import CATEGORY, INFORM_SUCCESS_URL
from Utils.exception import CaseInitException, CaseExecutingException
from report import generate_html
from report import constants as report_constants

LOGGING = logger.get_logger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--action", help="jenkins/mannual")
parser.add_argument("--url", help="apk download url when using jenkins")
parser.add_argument("--buildId", help="buildId when using jenkins")
parser.add_argument("--force_install", help="whether to force install apk", action="store_true")
parser.add_argument("--device", help="device id")
parser.add_argument("--suite", help="define test suite")
parser.add_argument("--upload", help="whether to upload the test result")
parser.add_argument("--csvDir", help="the path you want to store csv results, optional")
parser.add_argument("--branchName", help="the branchName your test apk generated from")

class Runner(object):

    isCreateCsv = True
    upload = True
    daily_run = True

    def __init__(self, device):
        self.case_list = {}
        self.ran = {}
        self.conf = None
        self.device = device
        self.force_install = False
        self.buildId = '0'
        self.suites = None
        self.url = ''
        self.batch_num = ''
        self.log_tag = ''
        self.category = []
        self.csvDir = ''
        self.branchName = ''

    def load(self, suites):
        self.case_list = {}
        try:
            self.conf = configparser.ConfigParser()
            self.conf.read('configRunner.ini', encoding='UTF-8')
            if suites:            # if --suite is passed, suite_list is defined by cmd
                suite_list = suites
            else:              # else suite_list is defined by configRunner.ini file
                suite_list = self.conf.items('suite')
            for suite in suite_list:
                if suite in self.case_list.keys():
                    continue
                self.case_list.update({
                    suite: {
                        'case_list': []
                    }
                })
                for env in self.conf.items(suite):
                    self.case_list.get(suite).update({
                        env[0]: env[1]
                    })
                for case in self.conf.items(self.conf.get(suite, 'case')):
                    self.case_list.get(suite).get('case_list').append(case[1])
                if str(self.case_list.get(suite).get("case")).__contains__(CATEGORY.BASIC.value):
                    self.category.append(CATEGORY.BASIC)
                if str(self.case_list.get(suite).get("case")).__contains__(CATEGORY.BIZ.value):
                    self.category.append(CATEGORY.BIZ)
        except Exception, e:
            self.case_list = {}
            LOGGING.exception(self.log_tag + 'config load error.')

    def start_case_copy(self, package, branch, app_version, f, suite):
        try:
            case = importlib.import_module(package.replace('/', '.') + '.' + f)
            reload(case)
        except Exception as e:
            LOGGING.exception(self.log_tag + "case load error: ")
            return

        try:
            c = case.Case(case.app, case.scene, self.buildId, branch, app_version, self.batch_num, self.device, self.ran, suite)
        except Exception as e:
            LOGGING.exception(self.log_tag + "case init fail at: ")
            if c.driver:
                if c.listener:
                    c.listener.stop()
                c.driver.quit()
                LOGGING.info(self.log_tag + "driver quit smoothly after case init fail")
            raise CaseInitException(self.batch_num + device + case.app + case.scene + ' init fail', e)

        try:
            adb_shell_cmd.press_back_twice(self.device)
            getattr(c, 'case')()
        except Exception as e:
            LOGGING.exception(self.log_tag + 'has exception when invoke case()')
            raise CaseExecutingException(self.batch_num + "_" + device + "_" + case.app + "_" + case.scene + ' execute fail', e)
        finally:
            try:
                if c.listener:
                    c.listener.stop()
                c.driver.quit()
                LOGGING.info(self.log_tag + "driver quit smoothly after case executed")
            except Exception:
                LOGGING.exception(self.log_tag + 'Exception occurs when quit the driver in finally.')

    def run(self):
        for suite in self.case_list.keys():

            if suite not in self.ran.keys():
                self.ran.update({
                    suite: {}
                })

            apk_location = os.path.abspath(os.path.join(os.path.dirname(__file__), self.case_list.get(suite).get('apk_location')))
            app_version = check_installed_version(device, self.force_install, self.case_list.get(suite).get('app'), self.case_list.get(suite).get('app_version'), apk_location, self.url, self.branchName, suite)
            loop_count = int(self.case_list.get(suite).get('loop'))
            for case in self.case_list.get(suite).get('case_list'):
                if case not in self.ran.get(suite):
                    self.ran.get(suite).update({
                        case: []
                    })
            analyzeThread = AnalyzePics(suite, self.category, self.device, self.ran, self.batch_num,
                                        self.buildId, Runner.upload)
            analyzeThread.start()
            while loop_count > 0:
                for case in self.case_list.get(suite).get('case_list'):
                    if case not in self.ran.get(suite):
                        self.ran.get(suite).update({
                            case: []
                        })

                    LOGGING.info(self.log_tag + 'running case: ' + self.case_list.get(suite).get('path') + '/' + case)
                    timeoutMonitorThread = timeoutMonitor.TimeoutMonitorThread(constants.CASETIMEOUT, self.device)
                    try:
                        if self.category == CATEGORY.BIZ:
                            timeoutMonitorThread.start()
                        self.start_case_copy(self.case_list.get(suite).get('path'), self.case_list.get(suite).get('branch'), app_version,
                                             case, suite)
                        timeoutMonitorThread.stop()
                    except Exception as e:
                        LOGGING.exception(self.log_tag + 'Exception occurs when calling start_case_copy, keep loop count unchanged to rerun')
                        timeoutMonitorThread.stop()
                    if self.category == CATEGORY.BIZ:
                        timeoutMonitorThread.join()
                # update loop when all case ran for one loop
                loop_count -= 1
            analyzeThread.stop()
            analyzeThread.join()
        self.logResponseTime()
        if Runner.isCreateCsv:
            self.generateReport()

    def generateReport(self):
        csvPath = self.get_csv_path(self.branchName)
        htmlPath = self.get_html_path(self.branchName)
        self.createCsv(csvPath)
        generate_html.generate_html(csvPath, htmlPath)


    def logResponseTime(self):
        LOGGING.info(self.log_tag + "all case:")
        for suite in self.ran.keys():
            LOGGING.info(self.log_tag + suite + ":")
            for case in self.ran.get(suite):
                LOGGING.info(self.log_tag + "    " + case + ":")
                for single_time_list in self.ran.get(suite).get(case):
                    if isinstance(single_time_list, list):
                        str_list = [str(i) for i in single_time_list]
                        LOGGING.info(self.log_tag + "        " + ", ".join(str_list))
                    else:
                        LOGGING.info(self.log_tag + "        " + str(single_time_list))

    def createCsv(self, csvPath):
        app_nameAndVersions = []
        for suite in self.ran.keys():
            app_nameAndVersions.append(self.case_list.get(suite).get('app') + '-' + self.case_list.get(suite).get('app_version'))
        versions_str = "+".join(app_nameAndVersions)
        result_dict = self.generateResultToRecordInCsv()
        self.recordInCsvForAllCases(csvPath, result_dict, versions_str)

    def get_csv_path(self, csvDir):
        if csvDir:
            csvPath = os.path.join(os.path.join(report_constants.CSV_DIR, csvDir))
        else:
            csvPath = os.path.join(os.path.join(report_constants.CSV_DIR, self.device), constants.ROOT_RESULT_DIR,
                                   constants.CSV_RESULT_DIR)
        if not os.path.exists(csvPath):
            os.makedirs(csvPath)
        return csvPath

    def get_html_path(self, branchName):
        if branchName:
            htmlPath = os.path.join(os.path.join(report_constants.HTML_DIR, branchName))
        else:
            htmlPath = report_constants.HTML_DIR
        if not os.path.exists(htmlPath):
            os.makedirs(htmlPath)
        return htmlPath

    def recordInCsvForAllCases(self, csvPath, result_dict, versions_str):
        for case in result_dict.get(result_dict.keys()[0]).keys():
            cols = pd.DataFrame()
            for app_version in result_dict.keys():
                cols[app_version] = result_dict.get(app_version).get(case)
                cols.to_csv(os.path.join(csvPath, self.device + "_" + self.batch_num + "_" + case.replace("_",
                                                                                                          "-") + "_" + versions_str + ".csv"),
                            encoding='utf-8', index=False)
        # for case in self.ran.get(self.ran.keys()[0]):
        #     self.recordOtherResults(case, csvPath, result_dict, versions_str)

    def generateResultToRecordInCsv(self):
        result_dict = {}

        for suite in self.ran.keys():
            result_dict[self.case_list.get(suite).get('app') + '-' + self.case_list.get(suite).get('app_version')] = {}
            for case in self.ran.get(suite):
                max_length = max(
                    len(self.ran.get(suite).get(case)) for suite in self.ran.keys() if case in self.ran.get(suite))

                if 'start' in case:
                    self.generateStartResults(case, 1, suite, result_dict, max_length)
                    self.generateStartResults(case, 2, suite, result_dict, max_length)
                    continue

                caseResults = []
                caseResults += self.ran.get(suite).get(case)

                caseResults = self.filter_with_boxplot(caseResults)
                finalCaseResults = caseResults + list(-1 for i in range(max_length - len(caseResults)))
                result_dict[self.case_list.get(suite).get('app') + '-' + self.case_list.get(suite).get('app_version')][case] = finalCaseResults
        return result_dict

    def filter_with_boxplot(self, caseResults):
        outliers = boxplot.getOutliers(caseResults)
        if outliers:
            LOGGING.info(self.log_tag + 'delete outliers: ' + ','.join(str(s) for s in outliers))
        caseResults = [x for x in caseResults if x not in outliers]
        return caseResults

    def generateStartResults(self, case, phase, suite, result_dict, max_length):
        converted_case = None
        index = None
        if phase == 1:
            converted_case = case + '-' + "white"
            index = 0
        elif phase == 2:
            converted_case = case + '-' + "total"
            index = 1
        value_version = []
        for results in self.ran.get(suite).get(case):
            if index is not None and isinstance(results, list) and len(results) - 1 >= index:
                value_version.append(results[index])
            else:
                value_version.append(-1)

        value_version = self.filter_with_boxplot(value_version)
        finalCaseResults = value_version + list(-1 for i in range(max_length - len(value_version)))
        if converted_case in self.case_list.get(suite).get('app') + '-' + self.case_list.get(suite).get('app_version'):
            result_dict[self.case_list.get(suite).get('app') + '-' + self.case_list.get(suite).get('app_version')][converted_case] = finalCaseResults


    def returnFinishedFlag(self):
        if Runner.upload:
            for c in self.category:
                payload = {'type': c.value, 'status': 'done', 'batchId': self.batch_num}
                response = requests.get(INFORM_SUCCESS_URL, params=payload)
                LOGGING.info(self.log_tag + "resonse status:" + str(response.status_code) + "response text:" + response.text)


def mockTestData():
    for suite in r.suites:
        r.ran[suite] = {}
        if suite == 'tencent_online':
            for case in r.case_list.get(suite).get('case_list'):
                if 'start' in case:
                    r.ran[suite][case] = [[2208,2520], [2210, 2520]]
                else:
                    r.ran[suite][case] = [2123,2012]
        elif suite == 'netease_grey_biz_old':
            for case in r.case_list.get(suite).get('case_list'):
                if 'start' in case:
                    r.ran[suite][case] = [[2218,1520], [2230, 1520], [2224,1444], [9223,1444]]
                else:
                    r.ran[suite][case] = [3133, 2334]


if __name__ == "__main__":
    args = parser.parse_args()
    if args.device:
        device = args.device
    else:
        device = 'SJE0217C28004070'
    logger.init_logging(device)
    r = Runner(device)
    r.batch_num = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    r.log_tag = '[' + r.batch_num + ']: ' + '[' + device + ']'
    if args.branchName:
        r.branchName = args.branchName
    if args.csvDir:
        r.csvDir = args.csvDir

    if args.action == 'jenkins':
        if args.url is None or args.branchName is None:
            parser.error("--action jenkins requires --url and --buildId.")
        else:
            r.url = args.url
            r.branchName = args.branchName
    if args.force_install:
        r.force_install = True
    if args.suite:
        suite_list = str(args.suite).split(',')
        r.suites = suite_list
    if args.upload:
        Runner.upload = args.upload
    try:
        r.load(r.suites)
        # mockTestData()
        # r.generateReport()
        r.run()
    except Exception, e:
        LOGGING.exception(r.log_tag + "exception in runner")
    finally:
        r.returnFinishedFlag()
