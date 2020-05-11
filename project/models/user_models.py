#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  user.py  
@Desc :  用户模板
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from pydantic import BaseModel, Field, constr
# User-defined Modules


class UserLogin(BaseModel):
    """用户登录模型
    """
    username: constr(strip_whitespace=True, min_length=6) = Field(..., title="用户名")
    password: constr(strip_whitespace=True, min_length=6) = Field(..., title="密码")
