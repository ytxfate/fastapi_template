#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  proj_base_model.py  
@Desc :  基本模型
'''

# Standard library imports
from datetime import datetime
# Third party imports
from pydantic import BaseModel
# Local application imports


class ProjectBaseModel(BaseModel):
    """
    基本模型(所有模型都继承于此模型)
    """

    class Config():
        anystr_strip_whitespace=True    # 去空
        use_enum_values=True    # 用枚举的 value 属性填充模型
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
