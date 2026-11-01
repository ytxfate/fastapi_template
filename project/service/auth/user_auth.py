#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  user_auth.py
@Desc :  用户认证
"""

import logging

from fastapi import APIRouter

from project.controller.proj_base_model import JWTBodyInfo
from project.utils import resp_code
from project.utils.jwt_auth import JWTAuth

logger = logging.getLogger("uvicorn")

user_auth = APIRouter()


async def srvc_user_login(
    username: str,
    password: str,
) -> tuple[resp_code.RespCode, str, str, str, dict]:
    logger.info("username: %s  password: %s", username, password)
    user_info = JWTBodyInfo(username=username, scopes=["info1"]).model_dump()
    status, jwt, refresh_jwt = JWTAuth().create_jwt_and_refresh_jwt(user_info)
    if status is False:
        return resp_code.JWT_CREATE_ERROR, "", "", "JWT 信息生成异常", {}
    return resp_code.SUCCESS, jwt, refresh_jwt, "", user_info


async def srvc_refresh_token(
    jwt: str,
    refresh_jwt: str,
) -> tuple[resp_code.RespCode, str, str, str]:
    decode_status, data = JWTAuth().decode_jwt_check_refresh_jwt(jwt, refresh_jwt)
    if decode_status is False:
        return resp_code.USER_NO_LOGIN, "", "", "刷新 jwt 失败，重新登录"

    status, new_jwt, new_refresh_jwt = JWTAuth().create_jwt_and_refresh_jwt(data)
    if status is False:
        return resp_code.JWT_CREATE_ERROR, "", "", "JWT 信息生成异常"

    return resp_code.SUCCESS, new_jwt, new_refresh_jwt, ""
