#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  operate_elasticsearch.py  
@Desc :  操作 elasticsearch 数据库
'''

# Standard library imports
import threading
from collections import namedtuple
import logging
# Third party imports
import elasticsearch
# Local application imports
from project.config.db_config import ELASTICSEARCH_CONF, ELASTICSEARCH_CONF_T
from project.config.sys_config import isFormalSystem

# ============================ 定义 MongoDB 连接配置 =========================== #
ELASTICSEARCH_CONF_NT = namedtuple("MONGODB_CONFIG", [
    "HOSTS",        # 连接地址
    "AUTH",         # AUTH 为 True 时需要进行 用户认证
    "USERNAME",     # 用户名
    "PASSWORD"      # 密码
])
# 设置默认值
ELASTICSEARCH_CONF_NT.__new__.__defaults__ = (
    [{'host': "127.0.0.1", "port": 9200}],
    False,
    "xxx",
    "xxx",
)
# ============================================================================ #

logger = logging.getLogger(__name__)

class OperateElasticsearch:
    """
    elasticsearch 数据库操作
    """
    _instance_lock = threading.Lock()

    conn_es = None
    
    def __init__(self, priority_conf: dict={}):
        """priority_conf 存在则优先使用
        """
        # 判断获取那个连接配置
        tmp_conf = priority_conf or (ELASTICSEARCH_CONF if isFormalSystem else ELASTICSEARCH_CONF_T)
        self.es_conf = ELASTICSEARCH_CONF_NT(**tmp_conf)
        logger.info(self.es_conf)


    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not hasattr(cls, '_instance'):
            with OperateElasticsearch._instance_lock:
                if not hasattr(cls, '_instance'):
                    OperateElasticsearch._instance = super().__new__(cls)
        return OperateElasticsearch._instance


    def __conn_elasticsearch(self):
        """
        连接 elasticsearch 数据库
            @return:
                elasticsearch_connection
        """
        conn_dict = {"hosts": self.es_conf.HOSTS}
        if self.es_conf.AUTH is True:
            # http_auth is tuple
            conn_dict['http_auth'] = (self.es_conf.USERNAME,
                                      self.es_conf.PASSWORD)
        self.conn_es = elasticsearch.Elasticsearch(**conn_dict)
        logger.info("elasticsearch connected.")


    def get_conn(self):
        """获取 elasticsearch_connection
        """
        if not self.conn_es:
            self.__conn_elasticsearch()
        return self.conn_es

    def __del__(self):
        try:
            self.conn_es.close()
        except:
            pass
        logger.info("elasticsearch closed.")
