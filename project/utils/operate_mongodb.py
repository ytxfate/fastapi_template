#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  operate_mongodb.py  
@Desc :  操作 MongoDB 数据库
'''

# Standard library imports
import threading
# Third party imports
import pymongo
# Local application imports
from project.config.db_config import MONGODB_CONF, MONGODB_CONF_T
from project.config.sys_config import isFormalSystem


class OperateMongodb:
    """
    MongoDB 数据库操作
    """
    _instance_lock = threading.Lock()

    def __init__(self):
        # 根据 isFormalSystem 判断连接哪个 mongo 数据库
        if isFormalSystem:
            self.MONGO_CONF = MONGODB_CONF
        else:
            self.MONGO_CONF = MONGODB_CONF_T
    
    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if not hasattr(cls, '_instance'):
            with OperateMongodb._instance_lock:
                if not hasattr(cls, '_instance'):
                    OperateMongodb._instance = super().__new__(cls)
        return OperateMongodb._instance
    
    def conn_mongodb(self):
        """
        连接 MongoDB 数据库
            @return:
                mongo_connection and mongo_database
        """
        if 'URL' in self.MONGO_CONF and self.MONGO_CONF['URL'] != '':
            conn = pymongo.MongoClient(host=self.MONGO_CONF['URL'])
        else:
            conn = pymongo.MongoClient(
                host=self.MONGO_CONF['HOST'], port=self.MONGO_CONF['PORT'])
        db = conn.get_database(self.MONGO_CONF['DEFAULT_DB'])
        if self.MONGO_CONF['AUTH'] is True:
            db.authenticate(
                self.MONGO_CONF['USERNAME'], self.MONGO_CONF['PASSWORD'])
        return conn, db
