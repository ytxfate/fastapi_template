#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  global_exception_handler.py
@Desc :  全局异常处理
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import logging
# User-defined Modules
from project.app import app
from project.utils.comm_ret import comm_ret
from project.utils import resp_code


logger = logging.getLogger("uvicorn")


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(request: Request, exc: RequestValidationError):
    logger.exception(exc)
    return comm_ret(
        code=resp_code.PARAMETER_ERROR,
        msg="请求参数异常",
        resp=exc.errors()
    )


@app.exception_handler(StarletteHTTPException)
async def handle_http_exception(request: Request, exc: StarletteHTTPException):
    logger.exception(exc)
    # 用户认证
    # 此处添加异常校验的原因是 project/dependencies/auth_depend.py 中自定义的
    # check_jwt 函数只能通过 raise 异常的方式返回结果
    if exc.status_code in [
        resp_code.JWT_PARSE_ERROR, resp_code.USER_NO_AUTHORITY, 
        resp_code.USER_NO_LOGIN
    ]:
        return comm_ret(code=exc.status_code, msg=exc.detail)
    
    return comm_ret(
        code=resp_code.EXCEPTION_ERROR,
        isSuccess=False,
        msg="HTTP Exception"
    )


@app.exception_handler(Exception)
async def handle_all_exception(request: Request, exc: Exception):
    logger.exception(exc)
    return comm_ret(
        code=resp_code.EXCEPTION_ERROR,
        isSuccess=False,
        msg="System Exception"
    )

