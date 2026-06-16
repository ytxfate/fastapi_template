#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  download_depend.py
@Desc :  下载认证
"""

import logging

from fastapi import Depends
from fastapi.security import SecurityScopes

from .auth_depend import _check

logger = logging.getLogger("uvicorn")


class DownloadTkDepend:
    def __init__(self) -> None:
        pass

    def __call__(self, tk: str) -> str:
        return tk


async def check_download_jwt(
    security_scopes: SecurityScopes, jwt: str = Depends(DownloadTkDepend())
):
    """通用 token 检验"""
    return _check(security_scopes, jwt)
