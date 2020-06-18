# -*- encoding=utf8 -*-
__author__ = "jayce"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

start_app('com.netease.newspro')
sleep(4.0)
touch((412,229))
sleep(3.0)