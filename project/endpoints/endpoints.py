#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  endpoints.py  
@Desc :  路由管理
'''

# Standard library imports

# Third party imports
from fastapi import APIRouter, Depends
# Local application imports
from project.dependencies.auth_depend import check_jwt
from project.modules.auth.user_auth import user_auth
from project.modules.info.info import info_router
from project.modules.user.user import user_router


api = APIRouter()


api.include_router(user_auth, prefix='/user_auth', tags=['认证'])
api.include_router(user_router, prefix='/user', tags=['示例接口'],
                   dependencies=[Depends(check_jwt)])
api.include_router(info_router, prefix="/info", tags=['示例接口Security/scopes'])
