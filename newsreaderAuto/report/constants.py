#!/usr/bin/env python
# -*- coding: utf-8 -*-

case_map = {
    'hotstart-white': '热启动白屏',
    'hotstart-total': '热启动完整',
    'list-refresh': '头条列表刷新',
    'tuji': '图集详情页加载',
    'shipin-luodi': '视频详情页加载',
    'shipin-shouzhen': '视频起播',
    'tuwen': '图文详情页加载',
    'coldstart-white': '冷启动白屏',
    'coldstart-total': '冷启动完整',
    'coldstart-newuser-white': '新用户白屏',
    'coldstart-newuser-total': '新用户完整',
}

device_map = {
    'XPU4C17112010268': '华为nova',
    '573a521e': '小米6',
    'iOS': 'iOS11_iPhone7p'
}

# 需要和jenkins job name相同
# HTML_DIR = r'E:\jenkinsWorkspace\workspace\Android performance mock test'
HTML_DIR = r'/Users/jayce/netease/jenkins/workspace/iOS-Performance-Test/HTML'
HTML_NAME = "performance_test_results.html"
CSV_DIR = r'/Users/jayce/netease/jenkins/workspace/iOS-Performance-Test/CSV'


app_map = {
    'netease': '网易新闻',
    'neteaseOldLauncher': '网易新闻',
    'neteasePatch': '网易新闻patch',
    'neteaseOpt': '网易新闻启动优化',
    'toutiao': '今日头条',
    'tencent': '腾讯新闻'
}