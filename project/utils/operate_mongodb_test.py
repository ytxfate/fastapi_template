#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  operate_mongodb_test.py
@Desc :
"""

from project.utils.operate_mongodb import OperateMongodb


class TestOperateMongodb:
    def test_conn(self):
        conn, db_mongo = OperateMongodb().get_conn_and_db()
        conn2, db_mongo2 = OperateMongodb().get_conn_and_db()
        assert id(conn) == id(conn2)

    def test_db_mongo(self):
        conn, db_mongo = OperateMongodb().get_conn_and_db()
        res = db_mongo.command("ping")
        assert res.get("ok", 0) == 1
