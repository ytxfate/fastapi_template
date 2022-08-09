#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  operate_mongodb.py  
@Desc :  操作 MongoDB 数据库
'''

# Standard library imports
import threading
from collections import namedtuple
import logging
# Third party imports
import pymongo
# Local application imports
from project.config.db_config import MONGODB_CONF, MONGODB_CONF_T
from project.config.sys_config import isFormalSystem

# ============================ 定义 MongoDB 连接配置 =========================== #
MONGODB_CONF_NT = namedtuple("MONGODB_CONFIG", [
    "URL",          # 有此项则优先用此项进行数据库连接
                    # 否则用 HOST 和 PORT 连接
    "HOST",         # 连接地址
    "PORT",         # 连接端口
    "AUTH",         # AUTH 为 True 时需要进行 用户认证
    "USERNAME",     # 用户名
    "PASSWORD",     # 密码
    "DEFAULT_DB"    # 默认数据库
])
# 设置默认值
MONGODB_CONF_NT.__new__.__defaults__ = ("",
                                        "127.0.0.1",
                                        27017,
                                        False,
                                        "xxx",
                                        "xxx",
                                        "xxx")
# ============================================================================ #

logger = logging.getLogger(__name__)

class __OperateMongodb:
    """
    MongoDB 数据库操作 基本类
    此方法不实现单例模式, 以适应多库连接操作
    """

    conn_mongo, db_mongo = None, None
    
    def __init__(self, priority_conf: dict={}):
        """priority_conf 存在则优先使用
        """
        # 判断获取那个连接配置
        tmp_conf = priority_conf
        self.mongodb_conf = MONGODB_CONF_NT(**tmp_conf)


    def __conn_mongodb(self):
        """
        连接 MongoDB 数据库
            @return:
                mongo_connection and mongo_database
        """
        if self.mongodb_conf.URL:
            self.conn_mongo = pymongo.MongoClient(host=self.mongodb_conf.URL)
        else:
            self.conn_mongo = pymongo.MongoClient(host=self.mongodb_conf.HOST,
                                                  port=self.mongodb_conf.PORT)
        self.db_mongo = self.conn_mongo.get_database(self.mongodb_conf.DEFAULT_DB)
        if self.mongodb_conf.AUTH is True:
            self.db_mongo.authenticate(self.mongodb_conf.USERNAME,
                                       self.mongodb_conf.PASSWORD)
        logger.info("mongodb connected: %s", self.mongodb_conf)


    def get_conn_and_db(self):
        """获取 mongo_connection 和 mongo_database
        """
        if (not self.conn_mongo) or (not self.db_mongo):
            self.__conn_mongodb()
        return self.conn_mongo, self.db_mongo


    def conn_mongodb(self):
        """兼容老代码
        """
        return self.get_conn_and_db()


    def __del__(self):
        try:
            self.conn_mongo.close()
        except:
            pass
        logger.info("mongodb closed.")



class OperateMongodb(__OperateMongodb):
    """MongoDB 数据库操作
    """
    _instance_lock = threading.Lock()
    def __init__(self, priority_conf: dict={}):
        """priority_conf 存在则优先使用
        """
        # 判断获取那个连接配置
        tmp_conf = priority_conf or (MONGODB_CONF if isFormalSystem else MONGODB_CONF_T)
        self.mongodb_conf = MONGODB_CONF_NT(**tmp_conf)
    
    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not hasattr(cls, '_instance'):
            with OperateMongodb._instance_lock:
                if not hasattr(cls, '_instance'):
                    OperateMongodb._instance = super().__new__(cls)
        return OperateMongodb._instance


class OperateMongodbxxx(__OperateMongodb):
    """MongoDB 数据库操作
    """
    _instance_lock = threading.Lock()
    def __init__(self, priority_conf: dict={}):
        """priority_conf 存在则优先使用
        """
        # 判断获取那个连接配置
        tmp_conf = priority_conf or (MONGODB_CONF if isFormalSystem else MONGODB_CONF_T)
        self.mongodb_conf = MONGODB_CONF_NT(**tmp_conf)
    
    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not hasattr(cls, '_instance'):
            with OperateMongodbxxx._instance_lock:
                if not hasattr(cls, '_instance'):
                    OperateMongodbxxx._instance = super().__new__(cls)
        return OperateMongodbxxx._instance
