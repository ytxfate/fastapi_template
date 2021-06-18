#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  opt_redis_sentinel.py  
@Desc :  操作 Redis 哨兵数据库集群
'''

# Standard library imports
import threading
# Third party imports
from redis.sentinel import Sentinel
# Local application imports
from project.config.db_config import (REDIS_SENTINELS_CONFIG_T,
                                      REDIS_SENTINELS_CONFIG)
from project.config.sys_config import isFormalSystem


class OptRedisSentinel:
    """
    操作 Redis 哨兵数据库集群
    """
    _instance_lock = threading.Lock()

    def __init__(self):
        # 根据 isFormalSystem 判断连接哪个 redis 数据库
        self.REDIS_CONFIG = REDIS_SENTINELS_CONFIG if isFormalSystem else REDIS_SENTINELS_CONFIG_T
        self.redis_master, self.redis_slave = None, None
        self.conn_kwargs = {}
        if self.REDIS_CONFIG['AUTH'] is True:
            self.conn_kwargs['password'] = self.REDIS_CONFIG['PASSWORD']


    def __conn_redis(self):
        sentinel = Sentinel(self.REDIS_CONFIG['SENTINELS'], socket_timeout=0.1,
                            decode_responses=self.REDIS_CONFIG['DECODE_RESPONSES'],
                            **self.conn_kwargs)
        self.redis_master = sentinel.master_for(self.REDIS_CONFIG['SERVICE_NAME'],
                                                socket_timeout=0.1)
        self.redis_slave = sentinel.slave_for(self.REDIS_CONFIG['SERVICE_NAME'],
                                              socket_timeout=0.1)

    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with OptRedisSentinel._instance_lock:
                if not hasattr(cls, '_instance'):
                    OptRedisSentinel._instance = super().__new__(cls)
        return OptRedisSentinel._instance
    
    def conn_redis(self):
        """
        连接 Redis 数据库
            @return:
                redis_master_connection, redis_slave_connection
        """
        if not(self.redis_master or self.redis_slave):
            self.__conn_redis()
        return self.redis_master, self.redis_slave
