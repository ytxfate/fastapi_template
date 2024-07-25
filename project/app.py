#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  app.py  
@Desc :  项目基本配置模块
'''

# Standard library imports
import logging
# Third party imports
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
# Local application imports
from project.config.sys_config import (prefix_api_path, isFormalSystem,
                                       API_DOC_DESC, API_DOC_TITLE,
                                       API_DOC_VERSION, app_run_conf)
from project.utils.api_limiter import api_user_limiter


logger = logging.getLogger("uvicorn")

# 判断是否展示接口文档
docs_url = (prefix_api_path + "/docs") if isFormalSystem is False else None
redoc_url = (prefix_api_path + "/redoc") if isFormalSystem is False else None
openapi_url = (prefix_api_path + "/openapi.json") if isFormalSystem is False else None

app = FastAPI(docs_url=docs_url, redoc_url=redoc_url, openapi_url=openapi_url,
              title=API_DOC_TITLE, description=API_DOC_DESC,
              version=API_DOC_VERSION)

# 接口限流
app.state.limiter = api_user_limiter


# 跨域处理
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 打印 api 文档路径
if isFormalSystem is False:
    logger.debug("%s api docs url: http://%s:%s%s", API_DOC_TITLE, app_run_conf['HOST'], app_run_conf['PORT'], docs_url)

# 添加接口
from project.endpoints.endpoints import api
app.include_router(api, prefix=prefix_api_path)


# 全局自定义异常处理
import project.interceptor.global_exception_handler
import project.interceptor.before_req

# ------------------------------------ 接口文档 ------------------------------------ #
# ====================================================== #
# ======== uvloop==0.14.0 会导致 contextvars 失效 ======== #
# ====================================================== #
from fastapi.openapi.utils import get_openapi
from project.config.api_json import API_JSON

def simplify_openapi() -> dict:
    # 1 用于日志记录
    openapi_json = get_openapi(title=API_DOC_TITLE, version=API_DOC_VERSION,
                                routes=app.routes)
    # 剔除部分用不到的字段, 精简大小
    # 1.1 接口描述部分
    if 'paths' in openapi_json:
        for _uri, _method_dict in openapi_json['paths'].items():
            for _method, _body in _method_dict.items():
                for n_k in ['requestBody', 'responses', 'parameters', 'security', 'operationId', 'description']:
                    if n_k in _body:
                        del openapi_json['paths'][_uri][_method][n_k]
    # 1.2 结构体描述部分
    for n_k in ['components']:
        if n_k in openapi_json:
            del openapi_json[n_k]
    
    API_JSON.set(openapi_json)
    logger.debug(API_JSON.get())
    return

simplify_openapi()
# ------------------------------------ 接口文档 ------------------------------------ #

# ------------------------------------ 全局后台任务(start) ------------------------------------ #
import asyncio


async def global_background_task_base():
    while 1:
        logger.debug("Background task is running...")
        await asyncio.sleep(5)
        raise ValueError('123')


async def global_background_task():
    while 1:
        try:
            await global_background_task_base()
        except Exception as e:
            logger.error("global_background_task: %s", e)
        await asyncio.sleep(1)


# 全局后台任务
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(global_background_task())
# ------------------------------------ 全局后台任务(end) ------------------------------------ #
