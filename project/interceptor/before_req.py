#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  before_req.py  
@Desc :  请求拦截器
'''

# Standard library imports
import logging
# Third party imports
from fastapi import Request
# Local application imports
from project.app import app
from project.utils import resp_code
from project.utils.comm_ret import comm_ret
from project.utils.jwt_auth import JWTAuth
from project.utils.operate_mongodb import OperateMongodb


logger = logging.getLogger("uvicorn")
_, db_mongo = OperateMongodb().conn_mongodb()

@app.middleware("http")
async def app_before_request(request: Request, call_next):
    # 按要求拦截请求
    path = request.url.path

    # 文档接口不拦截
    if "/docs" == path or '/openapi.json' == path or '/redoc' == path:
        return await call_next(request)
    return await call_next(request)
