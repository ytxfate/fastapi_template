#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  app.py
@Desc :  项目基本配置模块
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
# User-defined Modules
from project.config.sys_config import prefix_api_path, isFormalSystem

# 判断是否展示接口文档
docs_url = (prefix_api_path + "/docs") if isFormalSystem is False else None
redoc_url = (prefix_api_path + "/redoc") if isFormalSystem is False else None

app = FastAPI(docs_url=docs_url, redoc_url=redoc_url)

# 跨域处理
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 添加接口
from project.endpoints.endpoints import api
app.include_router(api, prefix=prefix_api_path)


# 全局自定义异常处理
import project.interceptor.global_exception_handler
import project.interceptor.before_req
