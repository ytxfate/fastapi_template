#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  auth_depend.py  
@Desc :  认证
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from pydantic import constr
from starlette.status import HTTP_401_UNAUTHORIZED
# User-defined Modules
from project.config.sys_config import prefix_api_path
from project.utils.comm_ret import comm_ret
from project.utils import resp_code
from project.utils.jwt_auth import JWTAuth
from project.models.auth_models import JWTBodyInfo


__oauth2_scheme = OAuth2PasswordBearer(tokenUrl=prefix_api_path+"/user_auth/login")


def check_jwt(jwt: constr(strip_whitespace=True)=Depends(__oauth2_scheme)):
    if not jwt:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail="用户未登录")
    # 解析 jwt 信息
    decode_status, user_info = JWTAuth().decode_jwt(jwt)
    if decode_status is False or not user_info:
        raise HTTPException(status_code=resp_code.JWT_PARSE_ERROR,
                            detail="刷新用户令牌中...")
    return JWTBodyInfo(**user_info)
