#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  user_models.py  
@Desc :  用户模板
'''

# Standard library imports

# Third party imports
from pydantic import BaseModel, Field, constr
# Local application imports


class UserLogin(BaseModel):
    """用户登录模型
    """
    username: constr(strip_whitespace=True, min_length=6) = Field(..., title="用户名")
    password: constr(strip_whitespace=True, min_length=6) = Field(..., title="密码")
