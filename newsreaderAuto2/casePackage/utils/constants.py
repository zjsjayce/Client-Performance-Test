#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "..")))
from enum import Enum

package = {
    "netease": "com.netease.newsreader.activity",
    "baidu": "com.baidu.searchbox",
    "toutiao": "com.ss.android.article.news",
    "tencent": 'com.tencent.news',
    "myapplication2":"com.example.zhaoyuting.myapplication2"
}

bclass = {
    "netease": "com.netease.nr.biz.ad.AdActivity",
    "baidu": "com.baidu.searchbox.SplashActivity",
    "tencent": "com.tencent.news.activity.SplashActivity",
    "toutiao": ".activity.MainActivity",
    "myapplication2": ".MainActivity"
}

huawei_device = ['DLQ0216408002491', 'SJE5T17429000361', 'SJE5T17623002873', 'MKJNW17C22011580', 'XPU4C17112010268', 'SJE0217C28004070', 'EJL4C17317001631']


device_map = {
    "573a521e": "小米6",
    "XPU4C17112010268": "华为nova"
}

appium_cmd = {
    "573a521e": "appium -p 4733 -bp 4734 --chromedriver-port 9525 --session-override --no-reset --log appium-573a521e-server-log --log-level debug",
    "XPU4C17112010268": "appium -p 4723 -bp 4724 --chromedriver-port 9515 --session-override --no-reset --log appium-XPU4C17112010268-server-log --log-level debug"
}

emmagee_dir = "/sdcard/Emmagee/"

AUTO_PATH = os.path.join('D:\\Users\\zhaoyuting', 'auto')

ROOT_RESULT_DIR = "performance"
BIZ_RESULT_DIR = "biz"
BASIC_RESULT_DIR = "basic"
UNCHECKED = "unchecked"
CSV_RESULT_DIR = "csvResults"

KEYCODE_BACk = 4
KEYCODE_HOME = 3

TEST_DURATION = 30 * 60


CASETIMEOUT = 10 * 60


class SCENE(Enum):
    COLDSTART = "coldstart"
    COLDSTART_AD = "coldstart-ad"
    COLDSTART_NEWUSER = "coldstart-newuser"
    COLDSTART_NEWUSER_AD = "coldstart-newuser-ad"
    COLDSTART_NOAD = "coldstart-noad"
    COLDSTART_NEWUSER__NOAD = "coldstart-newuser-noad"
    HOTSTART = "hotstart"
    HOTSTART_AD = "hotstart-ad"
    HOTSTART_NOAD = "hotstart-noad"
    LIST_REFRESH = "list-refresh"
    TUWEN = "tuwen"
    SHIPIN_LUODI = "shipin-luodi"
    SHIPIN_SHOUZHEN = "shipin-shouzhen"
    TUJI = "tuji"

class CATEGORY(Enum):
    BIZ = "biz"
    BASIC = "basic"

UPLOAD_FILE_URL = "http://qm.ws.netease.com/api/client/uploadFile"
INFORM_SUCCESS_URL = "http://qm.ws.netease.com/api/client/status"

FIND_FAIL_EXCE_MSG = "Didn't find wanted element"
RECORD_FAIL_EXCE_MSG = "Fail to record"

class MethodField(Enum):
    MethodName = "method_name"
    Threshold = "threshold"
    Sequence = "sequence"
    AddToMilestone = "add_to_milestone"


def getUploadScene(scene):
    # Caution! 必须先用==严格比较SCENE.COLDSTART_NOAD和SCENE.COLDSTART_AD的情况，否则SCENE.COLDSTART_NOAD，
    # SCENE.COLDSTART_AD都会命中 "coldstart" in str(self.scene)
    if scene == SCENE.COLDSTART_NOAD or scene == SCENE.COLDSTART_AD:
        return scene

    if scene == SCENE.HOTSTART_AD or scene == SCENE.HOTSTART_NOAD:
        return scene

    if scene == SCENE.COLDSTART_NEWUSER_AD or scene == SCENE.COLDSTART_NEWUSER__NOAD:
        return scene

    # after SCENE.COLDSTART_NOAD and SCENE.COLDSTART_AD, do the rest compare
    elif "newuser" in str(scene):
        return SCENE.COLDSTART_NEWUSER
    elif "coldstart" in str(scene):
        return SCENE.COLDSTART
    elif "hotstart" in str(scene):
        return SCENE.HOTSTART
    elif "refresh" in str(scene) and "list" in str(scene):
        return SCENE.LIST_REFRESH
    elif "shipin_luodi" in str(scene):
        return SCENE.SHIPIN_LUODI
    elif "tuji" in str(scene):
        return SCENE.TUJI
    elif "tuwen" in str(scene):
        return SCENE.TUWEN
    elif "shipin_shouzhen" in str(scene):
        return SCENE.SHIPIN_SHOUZHEN

