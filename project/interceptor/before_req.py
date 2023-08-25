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
from project.utils.sys_access_log import sys_access_log
from project.config.sys_config import prefix_api_path


logger = logging.getLogger("uvicorn")

@app.middleware("http")
async def app_before_request(request: Request, call_next):
    path = request.url.path
    # 文档接口不拦截
    if f"{prefix_api_path}/docs" == path or \
        f'{prefix_api_path}/openapi.json' == path or \
        f'{prefix_api_path}/redoc' == path:
        return await call_next(request)
    # 访问日志记录 
    # (取消注释 [文件头的库导入也需打开] 则生成日志信息,但并不保存,需自行选择存储方式)
    # 1 登录接口因为需要记录用户信息所以不能在此处记录
    # 2 下载文件的接口进行日志记录会导致服务阻塞
    if not(("/login" in path) or ('/download' in path)):
        await sys_access_log(request=request)
    return await call_next(request)
