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


logger = logging.getLogger(__name__)

# 判断是否展示接口文档
docs_url = (prefix_api_path + "/docs") if isFormalSystem is False else None
redoc_url = (prefix_api_path + "/redoc") if isFormalSystem is False else None
openapi_url = (prefix_api_path + "/openapi.json") if isFormalSystem is False else None

app = FastAPI(docs_url=docs_url, redoc_url=redoc_url, openapi_url=openapi_url,
              title=API_DOC_TITLE, description=API_DOC_DESC,
              version=API_DOC_VERSION)

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
