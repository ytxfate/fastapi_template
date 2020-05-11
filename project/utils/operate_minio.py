#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  operate_minio.py
@Desc :  操作 minio
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from minio import Minio
import threading
# User-defined Modules
from project.config.db_config import Minio_config, Minio_config_test
from project.config.sys_config import isFormalSystem


class OperateMinio:
    """
    操作 Minio
    """
    _instance_lock = threading.Lock()

    def __init__(self):
        if isFormalSystem:
            self.Minio_config = Minio_config
        else:
            self.Minio_config = Minio_config_test
    
    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not hasattr(cls, '_instance'):
            with OperateMinio._instance_lock:
                if not hasattr(cls, '_instance'):
                    OperateMinio._instance = super().__new__(cls)
        return OperateMinio._instance
    
    def conn_minio(self):
        """
        连接 Minio
            @return:
                Minio object
        """
        minioClient = Minio(self.Minio_config['URL'],
                  access_key=self.Minio_config['ACCESS_KEY'],
                  secret_key=self.Minio_config['SECRET_KEY'],
                  secure=True)
        return minioClient
