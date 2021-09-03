#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  sys_config.py
@Desc :  系统配置文件
'''

# ********** 运行配置 ********** #
# 基本运行配置
app_run_conf = {
    "HOST": "0.0.0.0",
    "PORT": 5000,
    "RELOAD": True,
    "WORKERS": 10,
    "DEBUG": True
}

SECRET_KEY = "xxx"

# ********** 生产 与 测试 系统切换 ********** #
# True : 生产系统
# False: 测试系统
isFormalSystem = False

# 接口前缀及版本控制
__version = "v1.0"
prefix_api_path = "/api/{version}".format(version=__version)

# api 文档描述
API_DOC_TITLE = "xxx"
API_DOC_DESC = "xxx"
API_DOC_VERSION = __version
