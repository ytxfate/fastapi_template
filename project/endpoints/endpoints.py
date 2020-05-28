#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  endpoints.py  
@Desc :  路由管理
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from fastapi import APIRouter, Depends
# User-defined Modules
from project.dependencies.auth_depend import check_jwt
from project.modules.auth.user_auth import user_auth
from project.modules.user.user import user_router


api = APIRouter()


api.include_router(user_auth, prefix='/user_auth', tags=['user_auth'])
api.include_router(user_router, prefix='/user', tags=['user'], dependencies=[Depends(check_jwt)])
