#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  operate_redis.py
@Desc :  操作 Redis 数据库
"""

import logging
import threading
import time
from collections import namedtuple

import redis

from project.config.db_config import REDIS_CONF, REDIS_CONF_T
from project.config.sys_config import isFormalSystem

# ============================= 定义 Redis 连接配置 ============================ #
REDIS_CONF_NT = namedtuple(
    "REDIS_CONFIG",
    [
        "HOST",  # 连接地址
        "PORT",  # 连接端口
        "AUTH",  # AUTH 为 True 时需要进行 用户认证
        "PASSWORD",  # 密码
        "DECODE_RESPONSES",  # 是否对查询结果进行编码处理
        "DEFAULT_DB",  # 默认数据库
    ],
)
# 设置默认值
REDIS_CONF_NT.__new__.__defaults__ = ("127.0.0.1", 6379, False, "xxx", True, 0)
# ============================================================================ #

logger = logging.getLogger(__name__)


class __OperateRedis:
    """
    操作 Redis 数据库
    """

    redis_cli: redis.Redis

    def __init__(self, priority_conf: dict = {}):
        """priority_conf 存在则优先使用"""
        # 判断获取那个连接配置
        tmp_conf = priority_conf
        self.redis_conf = REDIS_CONF_NT(**tmp_conf)
        self.__conn_redis()

    def __conn_redis(self, enforce: bool = False):
        if not hasattr(self, "redis_cli") or enforce is True:
            conn_params = {
                "host": self.redis_conf.HOST,
                "port": self.redis_conf.PORT,
                "decode_responses": self.redis_conf.DECODE_RESPONSES,
            }
            if self.redis_conf.AUTH is True:
                conn_params["password"] = self.redis_conf.PASSWORD
            pool = redis.ConnectionPool(**conn_params)
            self.redis_cli = redis.Redis(
                connection_pool=pool, db=self.redis_conf.DEFAULT_DB
            )
            logger.debug(self.redis_conf)
            logger.info("redis connected.")

    def reconnect(self):
        self.close()
        self.__conn_redis(True)

    def get_conn(self) -> redis.Redis:
        while 1:
            try:
                self.redis_cli.ping()
                break
            except redis.RedisError:
                time.sleep(1)
                self.reconnect()
        return self.redis_cli

    def close(self):
        try:
            self.redis_cli.close()
        except redis.RedisError:
            pass
        logger.info("redis closed.")

    def __del__(self):
        self.close()

    def conn_redis(self):
        """兼容老代码"""
        return self.get_conn()


class OperateRedis(__OperateRedis):
    """操作 Redis 数据库"""

    _instance_lock = threading.Lock()

    def __init__(self, priority_conf: dict = {}):
        """priority_conf 存在则优先使用"""
        super().__init__(
            priority_conf or (REDIS_CONF if isFormalSystem else REDIS_CONF_T)
        )

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not hasattr(cls, "_instance"):
            with OperateRedis._instance_lock:
                if not hasattr(cls, "_instance"):
                    OperateRedis._instance = super().__new__(cls)
        return OperateRedis._instance


class OperateRedisxxx(__OperateRedis):
    """操作 Redis 数据库"""

    _instance_lock = threading.Lock()

    def __init__(self, priority_conf: dict = {}):
        """priority_conf 存在则优先使用"""
        # 判断获取那个连接配置
        tmp_conf = priority_conf or (REDIS_CONF if isFormalSystem else REDIS_CONF_T)
        self.redis_conf = REDIS_CONF_NT(**tmp_conf)
        logger.debug(self.redis_conf)

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not hasattr(cls, "_instance"):
            with OperateRedisxxx._instance_lock:
                if not hasattr(cls, "_instance"):
                    OperateRedisxxx._instance = super().__new__(cls)
        return OperateRedisxxx._instance


if __name__ == "__main__":
    redis_cli = OperateRedis().get_conn()
    print(redis_cli, id(redis_cli))
    print(redis_cli.ping())
    redis_cli2 = OperateRedis().get_conn()
    print(redis_cli2, id(redis_cli2))
    print(redis_cli2.ping())
