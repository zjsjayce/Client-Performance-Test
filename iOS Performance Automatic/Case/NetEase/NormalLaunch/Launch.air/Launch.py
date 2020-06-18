# -*- encoding=utf8 -*-
__author__ = "jayce"

from airtest.core.api import *
from airtest.cli.parser import cli_setup


sleep(2.0)
start_app('com.netease.news')
sleep(3.0)
stop_app('com.netease.news')
sleep(2.0)



# script content


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath="/Users/jayce/PerformanceOutput/NetEase/Launch")