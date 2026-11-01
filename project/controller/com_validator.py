#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  com_validator.py
@Desc :  公共校验器
"""

import uuid
from datetime import datetime


# ==================== 默认值 ====================== #
def vldtr_default_false():
    """固定返回 False"""
    return False


def vldtr_default_true():
    """固定返回 True"""
    return True


def vldtr_default_none():
    """固定返回 None"""
    return None


def vldtr_default_uuid_hex():
    """固定返回 uuid7().hex"""
    return uuid.uuid7().hex


def vldtr_default_empty_list():
    """固定返回 []"""
    return []


def vldtr_default_empty_dict():
    """固定返回 {}"""
    return {}


def vldtr_default_now_datetime():
    """固定返回 {}"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ==================== 格式化 ====================== #
def vldtr_format_uuid_hex(v: uuid.UUID):
    """格式化返回 UUID1 的 hex 值"""
    return v.hex


def vldtr_format_float_2_decimal(v: float):
    """格式化 float 数据，保留两位小数"""
    return float("%.2f" % v)
