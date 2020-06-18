#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))


result_dict = {}
def collect_csv(csvDir):
    files = []
    devices = []
    cases = []
    app_versions = []
    for dirpath, dirnames, filenames in os.walk(csvDir):
        for file in filenames:
            if file.__contains__("csv"):
                files.append(os.path.join(dirpath, file))
                devices.append(file.split("_")[0])
                cases.append(file.split("_")[2])
                filename_nosuffix = os.path.splitext(file)[0]
                app_versions.extend(filename_nosuffix.split("_")[-1].split("+"))
    devices = set(devices)
    cases = set(cases)
    app_versions = set(app_versions)
    return files, devices, cases, app_versions

def computeAverageForAllCsv(filenames, devices, cases, app_versions):
    averageDict = {}
    result_each_csv_collection = []
    for filename in filenames:
        result_each_csv_collection.append(collectResultInEachCsv(filename))
    result_all = union_dict(result_each_csv_collection, devices, cases, app_versions)
    for case in result_all.keys():
        if (case not in averageDict.keys()):
            averageDict.update({case:{}})
        for device in result_all[case].keys():
            averageDict[case][device] = {}
            for app_version in result_all[case][device].keys():
                averageValue = getAverageValue(app_version, case, device, result_all)
                averageDict[case][device][app_version] = averageValue
    return averageDict


def getAverageValue(app_version, case, device, result_all):
    # remove -1 in result collection
    result_all[case][device][app_version] = [x for x in result_all[case][device][app_version] if x != -1]
    if result_all[case][device][app_version]:
        return sum(result_all[case][device][app_version]) / len(result_all[case][device][app_version])
    else:
        return 0


def union_dict(objs, devices, cases, app_versions):
    total = {}
    for case in cases:
        total[case] = {}
        for device in devices:
            total[case][device] = {}
            for app_version in app_versions:
                total[case][device][app_version] = []
    for obj in objs:
        for device in obj.keys():
            for case in obj[device].keys():
                device_case_once = obj[device][case]
                for app_version in device_case_once.keys():
                    device_case_app_once = device_case_once[app_version]
                    total[case][device][app_version].extend(device_case_app_once)
    return total


def collectResultInEachCsv(filename):
    device = filename.split("/")[-1].split("_")[0]
    case = filename.split("/")[-1].split("_")[2]
    result_dict_each_csv = {}
    result_dict_each_csv[device] = {case:{}}
    df = pd.read_csv(filename)
    app_verions_head = df.columns.tolist()
    for app_version in app_verions_head:
        result_dict_each_csv.get(device).get(case)[app_version] = df[app_version].values.tolist()
    return result_dict_each_csv

def generateResultToPlot(csvDir):
    filenames, devices, cases, app_versions = collect_csv(csvDir)
    final_result = computeAverageForAllCsv(filenames, devices, cases, app_versions)
    return final_result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csvDir", help="the path you want to store csv results, optional")
    args = parser.parse_args()
    generateResultToPlot(args.csvDir)
# for device in devices:
#     result_dict.update({device:{}})
#     for case in cases:
#         result_dict.get(device).update({case:{}})
#         for app_version in app_versions:
#             result_dict.get(device).get(case).update({app_version:-1})
