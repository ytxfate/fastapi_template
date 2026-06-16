#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  user_models.py
@Desc :  用户模板
"""

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class UserLogin(BaseModel):
    """用户登录模型"""

    username: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=6),
        Field(title="用户名"),
    ]
    password: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=6), Field(title="密码")
    ]
