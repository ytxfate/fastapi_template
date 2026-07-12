#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  endpoints.py
@Desc :  路由管理
"""

from fastapi import APIRouter, Depends

from project.controller.auth.user_auth import user_auth
from project.controller.info.info import info_router
from project.controller.user.user import user_router
from project.dependencies.auth_depend import check_jwt

api = APIRouter()


api.include_router(user_auth, prefix="/user_auth", tags=["认证"])
api.include_router(
    user_router, prefix="/user", tags=["示例接口"], dependencies=[Depends(check_jwt)]
)
api.include_router(info_router, prefix="/info", tags=["示例接口Security/scopes"])
