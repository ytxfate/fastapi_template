#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  sys_access_log.py  
@Desc :  系统访问日志记录
'''

# Standard library imports
import logging
# Third party imports
from fastapi import Request
from starlette.requests import Message
# Local application imports


logger = logging.getLogger("uvicorn")

async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}
    request._receive = receive


# async def get_body(request: Request) -> bytes:
#     body = await request.body()
#     await set_body(request, body)
#     return body


async def sys_access_log(request: Request):
    """系统访问日志记录
    """
    _body = await request.body()
    # 获取真实的 ip (可能存在 nginx 等方式的代理)
    ip = request.client.host
    __x_forwarded_for = request.headers.getlist("X-Forwarded-For") or []
    __x_real_ip = request.headers.getlist("X-Real-Ip") or None
    if __x_forwarded_for:
        ip = __x_forwarded_for[0]
    elif __x_real_ip:
        ip = __x_real_ip

    req_log_dict = {
        'uri': request.url.path,
        'method': request.method,
        'ip': ip,
        'url': request.url.components.geturl(),
        'query_params': request.query_params._dict,
        'path_params': request.path_params,
        'headers': request.headers.items(),
    }
    try:
        # 字符类参数可以进行编码存储
        req_log_dict['body'] = _body.decode()
    except Exception as e:
        logger.error(e)
        req_log_dict['body'] = f"** It could be a byte file ({e}) **"

    print(req_log_dict)   # 若要记录日志可在此处进行持久化操作
    
    await set_body(request, _body)
