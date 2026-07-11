#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  operate_minio.py
@Desc :  操作 minio
"""

import threading
from collections import namedtuple

from minio import Minio

from project.config.db_config import MINIO_CONFIG, MINIO_CONFIG_TEST
from project.config.sys_config import isFormalSystem

# ============================= 定义 Redis 连接配置 ============================ #
MINIO_CONFIG_NT = namedtuple(
    "MINIO_CONFIG",
    [
        "URL",  # 连接地址
        "ACCESS_KEY",  # KEY
        "SECRET_KEY",  # 密钥
    ],
)
# 设置默认值
MINIO_CONFIG_NT.__new__.__defaults__ = ("127.0.0.1", 6379, False, "xxx", True, 0)
# ============================================================================ #


class __OperateMinio:
    """
    操作 Minio
    """

    minio_cli: Minio

    def __init__(self, priority_conf: dict = {}):
        self.minio_conf = MINIO_CONFIG_NT(**priority_conf)
        self.__conn_minio()

    def __conn_minio(self):
        if not hasattr(self, "minio_cli"):
            self.minio_cli = Minio(
                self.minio_conf.URL,
                access_key=self.minio_conf.ACCESS_KEY,
                secret_key=self.minio_conf.SECRET_KEY,
                secure=False,  # use TLS or not
            )

    def get_conn(self) -> Minio:
        """
        连接 Minio
            @return:
                Minio object
        """
        return self.minio_cli


class OperateMinio(__OperateMinio):
    _instance_lock = threading.Lock()

    def __init__(self, priority_conf: dict = {}):
        """priority_conf 存在则优先使用"""
        super().__init__(
            priority_conf or (MINIO_CONFIG if isFormalSystem else MINIO_CONFIG_TEST)
        )

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not hasattr(cls, "_instance"):
            with OperateMinio._instance_lock:
                if not hasattr(cls, "_instance"):
                    OperateMinio._instance = super().__new__(cls)
        return OperateMinio._instance
