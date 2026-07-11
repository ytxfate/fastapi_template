#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  operate_elasticsearch.py
@Desc :  操作 elasticsearch 数据库
"""

import logging
import threading
import time
from collections import namedtuple

import elasticsearch

from project.config.db_config import ELASTICSEARCH_CONF, ELASTICSEARCH_CONF_T
from project.config.sys_config import isFormalSystem

# ============================ 定义 MongoDB 连接配置 =========================== #
ELASTICSEARCH_CONF_NT = namedtuple(
    "MONGODB_CONFIG",
    [
        "HOSTS",  # 连接地址
        "AUTH",  # AUTH 为 True 时需要进行 用户认证
        "USERNAME",  # 用户名
        "PASSWORD",  # 密码
    ],
)
# 设置默认值
ELASTICSEARCH_CONF_NT.__new__.__defaults__ = (
    [{"host": "127.0.0.1", "port": 9200}],
    False,
    "xxx",
    "xxx",
)
# ============================================================================ #

logger = logging.getLogger(__name__)


class __OperateElasticsearch:
    """
    elasticsearch 数据库操作
    """

    conn_es: elasticsearch.Elasticsearch

    def __init__(self, priority_conf: dict = {}):
        """priority_conf 存在则优先使用"""
        # 判断获取那个连接配置
        tmp_conf = priority_conf
        self.es_conf = ELASTICSEARCH_CONF_NT(**tmp_conf)

    def __conn_elasticsearch(self, enforce: bool = False):
        """
        连接 elasticsearch 数据库
            @return:
                elasticsearch_connection
        """
        if not hasattr(self, "conn_es") or enforce is True:
            conn_dict = {"hosts": self.es_conf.HOSTS}
            if self.es_conf.AUTH is True:
                # http_auth is tuple
                conn_dict["http_auth"] = (self.es_conf.USERNAME, self.es_conf.PASSWORD)
            self.conn_es = elasticsearch.Elasticsearch(**conn_dict)
            logger.debug(self.es_conf)
            logger.info("elasticsearch connected.")

    def reconnect(self):
        self.close()
        self.__conn_elasticsearch(True)

    def get_conn(self):
        """获取 elasticsearch_connection"""
        while 1:
            try:
                self.conn_es.ping()
                break
            except Exception:
                time.sleep(1)
                self.reconnect()
        return self.conn_es

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.conn_es.close()
        except Exception:
            pass
        logger.info("elasticsearch closed.")


class OperateElasticsearch(__OperateElasticsearch):
    """
    elasticsearch 数据库操作
    """

    _instance_lock = threading.Lock()

    def __init__(self, priority_conf: dict = {}):
        """priority_conf 存在则优先使用"""
        # 判断获取那个连接配置
        super().__init__(
            priority_conf
            or (ELASTICSEARCH_CONF if isFormalSystem else ELASTICSEARCH_CONF_T)
        )

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not hasattr(cls, "_instance"):
            with OperateElasticsearch._instance_lock:
                if not hasattr(cls, "_instance"):
                    OperateElasticsearch._instance = super().__new__(cls)
        return OperateElasticsearch._instance
