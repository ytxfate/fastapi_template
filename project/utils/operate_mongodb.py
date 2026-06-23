#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  operate_mongodb.py
@Desc :  操作 MongoDB 数据库
"""

import logging
import threading
import time
from collections import namedtuple
from typing import Tuple

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

from project.config.db_config import MONGODB_CONF, MONGODB_CONF_T
from project.config.sys_config import isFormalSystem

# ============================ 定义 MongoDB 连接配置 =========================== #
MONGODB_CONF_NT = namedtuple(
    "MONGODB_CONFIG",
    [
        "URL",  # 有此项则优先用此项进行数据库连接
        # 否则用 HOST 和 PORT 连接
        "HOST",  # 连接地址
        "PORT",  # 连接端口
        "AUTH",  # AUTH 为 True 时需要进行 用户认证
        "USERNAME",  # 用户名
        "PASSWORD",  # 密码
        "DEFAULT_DB",  # 默认数据库
    ],
)
# 设置默认值
MONGODB_CONF_NT.__new__.__defaults__ = (
    "",
    "127.0.0.1",
    27017,
    False,
    "xxx",
    "xxx",
    "xxx",
)
# ============================================================================ #

logger = logging.getLogger(__name__)


class __OperateMongodb:
    """
    MongoDB 数据库操作 基本类
    此方法不实现单例模式, 以适应多库连接操作
    """

    conn_mongo: MongoClient
    db_mongo: Database

    def __init__(self, priority_conf: dict = {}):
        """priority_conf 存在则优先使用"""
        # 判断获取那个连接配置
        tmp_conf = priority_conf
        self.mongodb_conf = MONGODB_CONF_NT(**tmp_conf)
        self.__conn_client()
        self.__conn_database()

    def __conn_client(self, enforce: bool = False):
        if not hasattr(self, "conn_mongo") or enforce is True:
            if self.mongodb_conf.URL:
                self.conn_mongo = MongoClient(host=self.mongodb_conf.URL)
            else:
                self.conn_mongo = MongoClient(
                    host=self.mongodb_conf.HOST,
                    port=self.mongodb_conf.PORT,
                )
            logger.debug("mongodb: %s", self.mongodb_conf)
            logger.info("mongodb connected(client)")

    def __conn_database(self, enforce: bool = False):
        if not hasattr(self, "db_mongo") or enforce is True:
            self.db_mongo = self.conn_mongo.get_database(self.mongodb_conf.DEFAULT_DB)
            if self.mongodb_conf.AUTH is True:
                self.db_mongo.authenticate(
                    self.mongodb_conf.USERNAME,
                    self.mongodb_conf.PASSWORD,
                )
            logger.info("mongodb connected(database)")

    def reconnect(self):
        self.close()
        self.__conn_client(True)
        self.__conn_database(True)

    def get_conn_and_db(self) -> Tuple[MongoClient, Database]:
        """获取 mongo_connection 和 mongo_database"""
        while 1:
            try:
                self.db_mongo.command("ping")
                break
            except ConnectionFailure:
                time.sleep(1)
                self.reconnect()
        return self.conn_mongo, self.db_mongo

    def close(self):
        try:
            self.conn_mongo.close()
        except Exception as e:
            logger.warning(e)
        logger.info("mongodb closed.")

    def __del__(self):
        self.close()

    def conn_mongodb(self):  # 兼容老代码
        return self.get_conn_and_db()


class OperateMongodb(__OperateMongodb):
    """MongoDB 数据库操作"""

    _instance_lock = threading.Lock()

    def __init__(self, priority_conf: dict = {}):
        """priority_conf 存在则优先使用"""
        super().__init__(
            priority_conf or (MONGODB_CONF if isFormalSystem else MONGODB_CONF_T)
        )

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not hasattr(cls, "_instance"):
            with OperateMongodb._instance_lock:
                if not hasattr(cls, "_instance"):
                    OperateMongodb._instance = super().__new__(cls)
        return OperateMongodb._instance


if __name__ == "__main__":
    conn, db_mongo = OperateMongodb().get_conn_and_db()
    print(conn, id(conn))
    print(db_mongo["test"].find_one())
    conn2, db_mongo2 = OperateMongodb().get_conn_and_db()
    print(conn2, id(conn2))
    print(db_mongo2["test"].find_one())
