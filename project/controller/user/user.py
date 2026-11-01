#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  user.py
@Desc :  用户
"""

from fastapi import APIRouter, Depends

from project.controller.proj_base_model import JWTBodyInfo
from project.dependencies.auth_depend import check_jwt
from project.utils.comm_ret import comm_ret

user_router = APIRouter()


@user_router.get("/")
def get_user_info(jwt_info: JWTBodyInfo = Depends(check_jwt)):
    print(jwt_info)
    return comm_ret(resp=jwt_info.model_dump())
