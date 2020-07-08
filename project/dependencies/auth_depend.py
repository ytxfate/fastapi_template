#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  auth_depend.py  
@Desc :  认证
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi.exceptions import HTTPException
from pydantic import constr
import logging
# User-defined Modules
from project.config.sys_config import prefix_api_path
from project.utils.comm_ret import comm_ret
from project.utils import resp_code
from project.utils.jwt_auth import JWTAuth
from project.models.auth_models import JWTBodyInfo


__oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=prefix_api_path+"/user_auth/login",
    scopes={"emp": "emp", "cus": "cus"},
    auto_error=False    # 不由 OAuth2PasswordBearer raise HTTPException
)

logger = logging.getLogger(__name__)

async def check_jwt(
    security_scopes: SecurityScopes,
    jwt: constr(strip_whitespace=True)=Depends(__oauth2_scheme)
):
    if not jwt:
        raise HTTPException(status_code=resp_code.USER_NO_LOGIN,
                            detail="用户未登录")
    # 解析 jwt 信息
    decode_status, user_info = JWTAuth().decode_jwt(jwt)
    if decode_status is False or not user_info:
        raise HTTPException(status_code=resp_code.JWT_PARSE_ERROR,
                            detail="刷新用户令牌中...")
    try:
        jwtbi = JWTBodyInfo(**user_info)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=resp_code.USER_NO_LOGIN,
                            detail="用户信息解析异常,请重新登录")
    
    # 检验 scopes
    if security_scopes.scopes:      # 判断是否需要检验 scopes
        user_scopes = jwtbi.scopes
        if set(user_scopes) >= set(security_scopes.scopes):
            return jwtbi
        else:
            raise HTTPException(status_code=resp_code.USER_NO_AUTHORITY,
                                detail="用户没有此接口的权限")
    else:
        return jwtbi
