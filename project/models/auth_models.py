#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  auth_models.py
@Desc :  认证
"""

from typing import Annotated

from pydantic import StringConstraints

from project.models.proj_base_model import ProjectBaseModel


class JWTBodyInfo(ProjectBaseModel):
    """jwt 中存储的信息"""

    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    scopes: list[
        Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    ] = []
