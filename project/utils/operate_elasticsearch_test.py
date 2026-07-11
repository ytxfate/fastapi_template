#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  operate_elasticsearch_test.py
@Desc :
"""

from project.utils.operate_elasticsearch import OperateElasticsearch


class TestOperateElasticsearch:
    def test_conn(self):
        conn = OperateElasticsearch().get_conn()
        conn2 = OperateElasticsearch().get_conn()
        assert id(conn) == id(conn2)

    def test_ping(self):
        conn = OperateElasticsearch().get_conn()
        assert conn.ping() is True
