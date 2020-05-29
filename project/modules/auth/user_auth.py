#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  user_auth.py  
@Desc :  用户认证
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from fastapi import APIRouter, Depends, Header, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from pydantic import constr
from datetime import datetime
import logging
# User-defined Modules
from project.utils.comm_ret import comm_ret
from project.models.auth_models import JWTBodyInfo
from project.utils.jwt_auth import JWTAuth
from project.utils import resp_code


logger = logging.getLogger(__name__)

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
    user_info = JWTBodyInfo(username="user").dict()
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
    Authorization: constr(strip_whitespace=True, min_length=1)=Header(..., title="jwt"),
    refresh_jwt: constr(strip_whitespace=True, min_length=1)=Query(..., title="refresh_jwt")
):
    # fastapi 在 Header Authorization 中加了前缀 Bearer
    scheme, Authorization = get_authorization_scheme_param(Authorization)
    if scheme.lower() != "bearer":
        return comm_ret(code=resp_code.JWT_PARSE_ERROR, msg="JWT 信息解析异常")
    # 校验 refresh_jwt 
    decode_status, _ = JWTAuth().decode_jwt(refresh_jwt)
    if decode_status is False:
        return comm_ret(
                code=resp_code.USER_NO_LOGIN, msg="刷新 jwt 失败，重新登录")
    # 解析 jwt
    user_info = JWTAuth().decode_jwt_without_check(Authorization)
    # 校验 user_info 不为空字典 {}
    try:
        JWTBodyInfo(**user_info)
    except Exception as e:
        logger.exception(e)
        return comm_ret(code=resp_code.JWT_PARSE_ERROR, msg="JWT 信息解析异常")
    
    status, new_jwt, new_refresh_jwt = JWTAuth().create_jwt_and_refresh_jwt(
        user_info)
    if status is False:
        return comm_ret(code=resp_code.JWT_CREATE_ERROR, msg="JWT 信息生成异常")

    return comm_ret(resp={'jwt': new_jwt, 'refresh_jwt': new_refresh_jwt})
