#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  download_depend.py  
@Desc :  下载认证
'''

# Standard library imports
import logging
# Third party imports
from fastapi import Depends
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import constr
# Local application imports
from project.config.sys_config import prefix_api_path
from project.models.auth_models import JWTBodyInfo
from project.utils import resp_code
from project.utils.comm_ret import comm_ret
from project.utils.jwt_auth import JWTAuth
from .auth_depend import _check


logger = logging.getLogger("uvicorn")


class DownloadTkDepend():
    def __init__(self) -> None:
        pass

    def __call__(self, tk: str) -> str:
        return tk


async def check_download_jwt(
    security_scopes: SecurityScopes,
    jwt: str=Depends(DownloadTkDepend())
):
    """ 通用 token 检验
    """
    return _check(security_scopes, jwt)
