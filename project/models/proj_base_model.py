#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  proj_base_model.py
@Desc :  基本模型
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectBaseModel(BaseModel):
    """
    基本模型(所有模型都继承于此模型)
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")},
    )
