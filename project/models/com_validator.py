#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  com_validator.py  
@Desc :  公共校验器
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from typing import Any
from pydantic import UUID1
import uuid
from datetime import datetime
# User-defined Modules

# ==================== 默认值 ====================== #
def vldtr_default_false(v: Any):
    """ 固定返回 False """
    return False

def vldtr_default_true(v: Any):
    """ 固定返回 True """
    return True

def vldtr_default_none(v: Any):
    """ 固定返回 None """
    return None

def vldtr_default_uuid_hex(v: UUID1):
    """ 固定返回 uuid1().hex """
    return uuid.uuid1().hex

def vldtr_default_empty_list(v: Any):
    """ 固定返回 [] """
    return []

def vldtr_default_empty_dict(v: Any):
    """ 固定返回 {} """
    return {}

def vldtr_default_now_datetime(v: Any):
    """ 固定返回 {} """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ==================== 格式化 ====================== #
def vldtr_format_uuid_hex(v: UUID1):
    """ 格式化返回 UUID1 的 hex 值 """
    return v.hex

def vldtr_format_float_2_decimal(v: float):
    """ 格式化 float 数据，保留两位小数 """
    return float('%.2f' % v)
