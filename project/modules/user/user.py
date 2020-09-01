#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  user.py  
@Desc :  用户
'''

# Standard library imports

# Third party imports
from fastapi import APIRouter, Depends
# Local application imports
from project.dependencies.auth_depend import check_jwt
from project.models.auth_models import JWTBodyInfo
from project.utils import resp_code
from project.utils.comm_ret import comm_ret


user_router = APIRouter()

@user_router.get("/")
def get_user_info(
    jwt_info: JWTBodyInfo=Depends(check_jwt)
):
    print(jwt_info)
    return comm_ret(resp=jwt_info.dict())
