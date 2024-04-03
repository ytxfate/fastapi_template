#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  api_limiter.py  
@Desc :  接口限流
'''

# Standard library imports

# Third party imports
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.requests import Request
from fastapi.security.utils import get_authorization_scheme_param
# Local application imports
from project.utils.jwt_auth import JWTAuth


def get_limit_key(request: Request) -> str:
    """限流key获取"""
    # 获取用户 JWT 中的信息
    auth_str = request.headers.get("Authorization") or ""
    _, jwt = get_authorization_scheme_param(auth_str)
    _, user_info = JWTAuth().decode_jwt(jwt, False)
    return f"{request.method}:{request.url.path}:{user_info.get('username', 'none')}"


api_user_limiter = Limiter(key_func=get_limit_key)  # 此处建议不要使用redis做存储
                                                    # 会产生redis请求键命中率低的警告
                                                    # 但不影响redis实际使用
