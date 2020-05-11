#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  endpoints.py  
@Desc :  路由管理
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from fastapi import APIRouter
# User-defined Modules
from project.modules.auth.user_auth import user_auth


api = APIRouter()


api.include_router(user_auth, prefix='/auth_user', tags=['auth_user'])
