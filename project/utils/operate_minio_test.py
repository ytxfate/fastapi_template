#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  operate_minio_test.py
@Desc :
"""

from project.utils.operate_minio import OperateMinio


class TestOperateMinio:
    def test_conn(self):
        conn = OperateMinio().get_conn()
        conn2 = OperateMinio().get_conn()
        assert id(conn) == id(conn2)
