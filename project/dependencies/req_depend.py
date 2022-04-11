#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  req_depend.py  
@Desc :  获取请求 Request 对象
'''

# Standard library imports
# Third party imports
from fastapi.requests import Request
from fastapi import Depends
# Local application imports

class ReqDepend():
    def __init__(self) -> None:
        pass

    def __call__(self, request: Request) -> Request:
        return request

req_depend = ReqDepend()
