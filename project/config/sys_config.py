#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  sys_config.py
@Desc :  系统配置文件
'''

# ********** 运行配置 ********** #
# 基本运行配置
app_run_conf = {
    "HOST": "127.0.0.1",
    "PORT": 5000,
    "RELOAD": True,
    "WORKERS": 1,
    "DEBUG": True
}

SECRET_KEY = "xxx"

# ********** 生产 与 测试 系统切换 ********** #
# True : 生产系统
# False: 测试系统
isFormalSystem = False
