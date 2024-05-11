#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  auth_depend.py  
@Desc :  认证
'''

# Standard library imports
import logging
# Third party imports
from fastapi import Depends
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import constr
# Local application imports
from project.config.sys_config import prefix_api_path
from project.models.auth_models import JWTBodyInfo
from project.utils import resp_code
from project.utils.comm_ret import comm_ret
from project.utils.jwt_auth import JWTAuth


_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=prefix_api_path+"/user_auth/login",
    scopes={"emp": "emp", "cus": "cus"},
    auto_error=False    # 不由 OAuth2PasswordBearer raise HTTPException
)

logger = logging.getLogger("uvicorn")

def _check(
    security_scopes: SecurityScopes,
    jwt: constr(strip_whitespace=True),
    jwt_stat: constr(strip_whitespace=True)=""
):
    """ token 检验
    """
    if not jwt:
        raise HTTPException(status_code=resp_code.USER_NO_LOGIN,
                            detail="用户未登录")
    # 解析 jwt 信息
    if jwt_stat == "NOT":
        decode_status, user_info = JWTAuth().decode_jwt(jwt, False)
    else:
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

async def check_jwt(
    req: Request,
    security_scopes: SecurityScopes,
    jwt: constr(strip_whitespace=True)=Depends(_oauth2_scheme),
):
    """ 通用 token 检验
    """
    print('check_jwt', req, req.url.path)
    return _check(security_scopes, jwt)


async def not_realy_check_jwt(
    security_scopes: SecurityScopes,
    jwt: constr(strip_whitespace=True)=Depends(_oauth2_scheme)
):
    """ 刷新 token 时调用
    """
    return _check(security_scopes, jwt, "NOT")

