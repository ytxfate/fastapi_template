#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  global_exception_handler.py  
@Desc :  全局异常处理
'''

# Standard library imports
import logging
# Third party imports
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from slowapi.errors import RateLimitExceeded
# Local application imports
from project.app import app
from project.utils import resp_code
from project.utils.comm_ret import comm_ret
from project.config.sys_config import isFormalSystem


logger = logging.getLogger("uvicorn")

class ParamsValueError(ValueError):
    """自定义参数校验异常  
    此异常提示信息将整合进统一返回的 msg 中
    """
    pass


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(request: Request, exc: RequestValidationError):
    logger.error(exc)
    # 自定义异常提示
    msg = set()
    for err in exc.errors():
        if err['type'] == "value_error.paramsvalue":
            msg.add(err['msg'])
    resp = {}
    if not isFormalSystem:
        resp = exc.errors()
        
    return comm_ret(
        code=resp_code.PARAMETER_ERROR,
        msg="\n".join(msg) or "请求参数异常",
        resp=resp
    )


@app.exception_handler(StarletteHTTPException)
async def handle_http_exception(request: Request, exc: StarletteHTTPException):
    logger.error(exc)
    # slowapi 接口限流
    if isinstance(exc, RateLimitExceeded):
        return comm_ret(
            code=resp_code.API_LIMIT,
            isSuccess=False,
            msg="限流"
        )
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
    logger.error(exc)
    return comm_ret(
        code=resp_code.EXCEPTION_ERROR,
        isSuccess=False,
        msg="System Exception"
    )

