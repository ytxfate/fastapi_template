#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  api_json.py  
@Desc :  接口文档: 来源于 openapi.json
'''

from contextvars import ContextVar

API_JSON = ContextVar("API_JSON")
API_JSON.set({})    # 初始化
"""
API_JSON 格式如下:
{
    "openapi": "3.0.2",
    "info": {
        "title": "xxx",
        "version": "v1.0"
    },
    "paths": {
        "/api/v1.0/user_auth/login": {
            "post": {
                "tags": [
                    "认证"
                ],
                "summary": "登录"
            }
        },
        "/api/v1.0/user_auth/refresh_token": {
            "get": {
                "tags": [
                    "认证"
                ],
                "summary": "刷新 Token 信息"
            }
        }
    }
}
"""
