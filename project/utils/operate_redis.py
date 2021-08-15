#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  operate_redis.py  
@Desc :  操作 Redis 数据库
'''

# Standard library imports
from collections import namedtuple
import logging
import threading
# Third party imports
import redis
# Local application imports
from project.config.db_config import REDIS_CONF, REDIS_CONF_T
from project.config.sys_config import isFormalSystem


# ============================= 定义 Redis 连接配置 ============================ #
REDIS_CONF_NT = namedtuple("Redis_CONFIG", [
    "HOST",         # 连接地址
    "PORT",         # 连接端口
    "AUTH",         # AUTH 为 True 时需要进行 用户认证
    "PASSWORD",     # 密码
    "DECODE_RESPONSES", # 是否对查询结果进行编码处理
    "DEFAULT_DB"    # 默认数据库
])
# 设置默认值
REDIS_CONF_NT.__new__.__defaults__ = ("127.0.0.1",
                                      6379,
                                      False,
                                      "xxx",
                                      True,
                                      0)
# ============================================================================ #


class OperateRedis:
    """
    操作 Redis 数据库
    """
    _instance_lock = threading.Lock()

    redis_cli = None

    def __init__(self, priority_conf: dict={}):
        """priority_conf 存在则优先使用
        """
        # 判断获取那个连接配置
        tmp_conf = priority_conf or (REDIS_CONF if isFormalSystem else REDIS_CONF_T)
        self.redis_conf = REDIS_CONF_NT(**tmp_conf)
        logging.info(self.redis_conf)
    
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with OperateRedis._instance_lock:
                if not hasattr(cls, '_instance'):
                    OperateRedis._instance = super().__new__(cls)
        return OperateRedis._instance

    
    def __conn_redis(self):
        """
        连接 Redis 数据库
            @return:
                redis_connection
        """
        if self.redis_conf.AUTH is True:
            pool = redis.ConnectionPool(
                host=self.redis_conf.HOST,
                port=self.redis_conf.PORT,
                password=self.redis_conf.PASSWORD,
                decode_responses=self.redis_conf.DECODE_RESPONSES
            )
        else:
            pool = redis.ConnectionPool(
                host=self.redis_conf.HOST,
                port=self.redis_conf.PORT,
                decode_responses=self.redis_conf.DECODE_RESPONSES
            )
        self.redis_cli = redis.Redis(connection_pool=pool, db=self.redis_conf.DEFAULT_DB)
        logging.info("redis connected.")


    def get_conn(self):
        if not self.redis_cli:
            self.__conn_redis()
        return self.redis_cli


    def conn_redis(self):
        """兼容老代码
        """
        return self.get_conn()


    def __del__(self):
        try:
            self.redis_cli.close()
        except:
            pass
        logging.info("redis closed.")
