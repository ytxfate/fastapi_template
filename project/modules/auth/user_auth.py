#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  user_auth.py  
@Desc :  用户认证
'''

# The Python Standard Modules(Library) and Third Modules(Library)
from fastapi import APIRouter
# User-defined Modules
from project.models.user_models import UserLogin
from project.utils.comm_ret import comm_ret


user_auth = APIRouter()


@user_auth.post('/login')
def user_login(login_info:UserLogin):
    """
    用户登录
    """
    return comm_ret(resp=login_info.dict())
