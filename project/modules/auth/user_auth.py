#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  user_auth.py  
@Desc :  用户认证
'''

# Standard library imports
from datetime import datetime
import logging
# Third party imports
from fastapi import APIRouter, Depends, Header, Query
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import constr
from starlette.status import HTTP_401_UNAUTHORIZED
# Local application imports
from project.dependencies.auth_depend import (check_jwt, not_realy_check_jwt,
                                              _oauth2_scheme)
from project.models.auth_models import JWTBodyInfo
from project.utils import resp_code
from project.utils.comm_ret import comm_ret
from project.utils.jwt_auth import JWTAuth


logger = logging.getLogger("uvicorn")

user_auth = APIRouter()


@user_auth.post('/login', name="登录")
def user_login(login_info: OAuth2PasswordRequestForm=Depends()):
    """用户登录  
    code 返回 1200 重新登录;  
    code 返回 200 时, resp 中返回 jwt 及 refresh_jwt 信息;  
    jwt 用于验证用户登录;  
    当 访问系统所有需要认证的接口并返回 1102 时, 使用 refresh_jwt 刷新 jwt 及 refresh_jwt 信息;
    当返回 1101 时, jwt 生成异常, 再次发起请求 (基本不需要)

    即 code == 1102 , 需刷新 jwt;  
    code == 1200 , 需重新登录后跳转;  
    code == 1101 , 再次请求; (基本不需要)  
    """
    user_info = JWTBodyInfo(username="user", scopes=['info1']).dict()
    status, jwt, refresh_jwt = JWTAuth().create_jwt_and_refresh_jwt(user_info)
    if status is False:
        return comm_ret(
            code=resp_code.JWT_CREATE_ERROR, msg="JWT 信息生成异常")
    
    return JSONResponse(content=jsonable_encoder({
        "code": resp_code.SUCCESS,
        "isSuccess": True,
        "msg": "请求成功",
        "resp": {
            'jwt': jwt,
            'refresh_jwt': refresh_jwt
        },
        'access_token': jwt
    }))


@user_auth.get("/refresh_token", name="刷新 Token 信息")
def refresh_token(
    jwt: constr(strip_whitespace=True)=Depends(_oauth2_scheme),
    refresh_jwt: constr(strip_whitespace=True, min_length=1)=Query(..., title="refresh_jwt")
):
    decode_status, data = JWTAuth().decode_jwt_check_refresh_jwt(jwt,
                                                                 refresh_jwt)
    if decode_status is False:
        return comm_ret(code=resp_code.USER_NO_LOGIN,
                        msg="刷新 jwt 失败，重新登录")
    
    status, new_jwt, new_refresh_jwt = JWTAuth().create_jwt_and_refresh_jwt(
        data)
    if status is False:
        return comm_ret(code=resp_code.JWT_CREATE_ERROR, msg="JWT 信息生成异常")

    return comm_ret(resp={'jwt': new_jwt, 'refresh_jwt': new_refresh_jwt})
