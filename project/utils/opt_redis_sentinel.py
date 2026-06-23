#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  opt_redis_sentinel.py
@Desc :  操作 Redis 哨兵数据库集群
"""

import logging
import threading
from collections import namedtuple
from typing import Tuple, Union

from redis import Redis
from redis.exceptions import ConnectionError, RedisError, TimeoutError
from redis.sentinel import Sentinel

from project.config.db_config import REDIS_SENTINELS_CONFIG, REDIS_SENTINELS_CONFIG_T
from project.config.sys_config import isFormalSystem

logger = logging.getLogger(__name__)

# ============================= 定义连接配置 ============================ #
REDIS_SENTINEL_CONF_NT = namedtuple(
    "REDIS_SENTINEL_CONF",
    [
        "SENTINELS",  # ip端口集合
        "SERVICE_NAME",  # 服务名称
        "PASSWORD",  # 密码
        "SENTINEL_PWD",  # sentinel 密码
        "DECODE_RESPONSES",  # 解码
        "DB",
    ],
)
# 设置默认值
REDIS_SENTINEL_CONF_NT.__new__.__defaults__ = (
    [("127.0.0.1", 6379)],
    "mymaster",
    None,
    None,
    True,
    0,
)
# ============================================================================ #


class __OptRedisSentinel:
    """
    操作 Redis 哨兵数据库集群
    """

    _instance_lock = threading.Lock()
    master: Redis
    slave: Redis

    def __init__(self, conf: Union[dict, REDIS_SENTINEL_CONF_NT]):
        if isinstance(conf, REDIS_SENTINEL_CONF_NT):
            self.conf = conf
        else:
            self.conf = REDIS_SENTINEL_CONF_NT(**conf)

        self.conn_kwargs = {
            "db": self.conf.DB,
            "socket_timeout": 1,
            "retry_on_timeout": True,
            "health_check_interval": 10,
            "socket_connect_timeout": 5,
            "retry_on_error": [RedisError, ConnectionError, TimeoutError],
        }
        self.sentinel_kwargs = {
            "socket_timeout": 1,
            "retry_on_timeout": True,
            "health_check_interval": 10,
            "socket_connect_timeout": 5,
            "retry_on_error": [RedisError, ConnectionError, TimeoutError],
        }
        if self.conf.PASSWORD:
            self.conn_kwargs["password"] = self.conf.PASSWORD
        if self.conf.SENTINEL_PWD:
            self.sentinel_kwargs["password"] = self.conf.SENTINEL_PWD
        logger.debug(self.conf)

    def __conn_redis(self):
        sentinel = Sentinel(
            self.conf.SENTINELS,
            sentinel_kwargs=self.sentinel_kwargs,
            decode_responses=self.conf.DECODE_RESPONSES,
            **self.conn_kwargs,
        )
        self.master = sentinel.master_for(
            self.conf.SERVICE_NAME,
        )
        self.slave = sentinel.slave_for(
            self.conf.SERVICE_NAME,
        )

    def conn_redis(self) -> Tuple[Redis, Redis]:
        """
        连接 Redis 数据库
            @return:
                redis_master_connection, redis_slave_connection
        """
        if not hasattr(self, "master") or not hasattr(self, "slave"):
            self.__conn_redis()
        return self.master, self.slave


class OptRedisSentinel(__OptRedisSentinel):
    """redis 哨兵连接工具

    注:
        实时性要求高的操作在 master 上执行读写操作
        实时性要求低的操作在 master 上执行写操作, slave 上执行读操作
    """

    _instance_lock = threading.Lock()

    def __init__(self):
        super().__init__(
            REDIS_SENTINELS_CONFIG if isFormalSystem else REDIS_SENTINELS_CONFIG_T
        )

    def __new__(cls, *args, **kwargs):
        """单例"""
        if not hasattr(cls, "_instance"):
            with OptRedisSentinel._instance_lock:
                if not hasattr(cls, "_instance"):
                    OptRedisSentinel._instance = super().__new__(cls)
        return OptRedisSentinel._instance
