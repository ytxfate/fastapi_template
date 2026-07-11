#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  operate_redis_test.py
@Desc :
"""

from project.utils.operate_redis import OperateRedis


class TestOperateRedis:
    def test_conn(self):
        redis_cli = OperateRedis().get_conn()
        redis_cli2 = OperateRedis().get_conn()
        assert id(redis_cli) == id(redis_cli2)

    def test_redis_cli(self):
        redis_cli = OperateRedis().get_conn()
        assert redis_cli.ping() is True
