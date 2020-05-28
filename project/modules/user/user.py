#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  user.py  
@Desc :  用户
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from fastapi import APIRouter, Depends
# User-defined Modules
from project.models.auth_models import JWTBodyInfo
from project.utils.comm_ret import comm_ret
from project.utils import resp_code
from project.dependencies.auth_depend import check_jwt


user_router = APIRouter()

@user_router.get("/")
def get_user_info(
    jwt_info: JWTBodyInfo=Depends(check_jwt)
):
    print(jwt_info)
    return comm_ret(resp=jwt_info.dict())
