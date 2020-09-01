#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  info.py  
@Desc :  测试信息
'''

# Standard library imports

# Third party imports
from fastapi import APIRouter, Security
# Local application imports
from project.dependencies.auth_depend import check_jwt
from project.models.auth_models import JWTBodyInfo
from project.utils import resp_code
from project.utils.comm_ret import comm_ret


info_router = APIRouter()

@info_router.get("/")
def info(
    jwtbi: JWTBodyInfo=Security(check_jwt, scopes=['info1'])
):
    return comm_ret(resp=jwtbi.dict())

@info_router.get("/info2")
def info2(
    jwtbi: JWTBodyInfo=Security(check_jwt, scopes=['info2'])
):
    return comm_ret(resp=jwtbi.dict())
