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
from fastapi import APIRouter, Depends, Header, Query, Request
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
from project.utils.sys_access_log import sys_access_log, SysLogModel
from project.config.api_json import API_JSON


logger = logging.getLogger("uvicorn")

user_auth = APIRouter()


@user_auth.post('/login', name="登录")
async def user_login(request: Request, 
            login_info: OAuth2PasswordRequestForm=Depends()):
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
    # ================== 日志记录 ================== #
    # 获取真实的 ip (可能存在 nginx 等方式的代理)
    ip = request.client.host
    __x_forwarded_for = request.headers.getlist("X-Forwarded-For") or []
    __x_real_ip = request.headers.getlist("X-Real-Ip") or None
    if __x_forwarded_for:
        ip = __x_forwarded_for[0]
    elif __x_real_ip:
        ip = __x_real_ip

    api_info = API_JSON.get().get('paths', {}).get(request.url.path, {})\
        .get(request.method.lower(), {})
    _body = {
        'grant_type': login_info.grant_type,
        'username': login_info.username,
        'password': login_info.password,
        'scopes': login_info.scopes,
        'client_id': login_info.client_id,
        'client_secret': login_info.client_secret,
    }
    await sys_access_log(slm=SysLogModel(
        uri=request.url.path,
        method=request.method,
        ip=ip,
        url=request.url.components.geturl(),
        headers=request.headers.items(),
        query_params=request.query_params._dict,
        path_params=request.path_params,
        body="&".join([f"{k}={v}" for k, v in _body.items() if v]), # 过滤掉空值
        tags=";".join(api_info.get("tags", [])),
        summary=api_info.get("summary", ""),
        user_info=user_info,
    ))
    # ============================================== #
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
