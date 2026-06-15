#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  sys_access_log.py
@Desc :  系统访问日志记录
"""

import dataclasses
import logging
from typing import ClassVar, List, Optional

from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import Field, StringConstraints, field_validator
from starlette.types import Receive
from typing_extensions import Annotated

from project.config.api_json import API_JSON
from project.models.com_validator import vldtr_default_now_datetime
from project.models.proj_base_model import ProjectBaseModel
from project.utils.jwt_auth import JWTAuth

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class ReceiveProxy:
    """Proxy to starlette.types.Receive.__call__ with caching first receive call."""

    receive: Receive
    cached_body: bytes
    _is_first_call: ClassVar[bool] = True

    async def __call__(self):
        # First call will be for getting request body => returns cached result
        if self._is_first_call:
            self._is_first_call = False
            return {
                "type": "http.request",
                "body": self.cached_body,
                "more_body": False,
            }

        return await self.receive()


async def get_request_body(request: Request) -> bytes:
    body = await request.body()
    request._receive = ReceiveProxy(receive=request.receive, cached_body=body)
    return body


SYS_ACCESS_LOG_COLL_NAME = "sys_access_log"
NEED_REMOVE_HEADERS = [  # 需要移除的请求头信息
    "connection",
]


class SysLogModel(ProjectBaseModel):
    """日志模型"""

    uri: Annotated[str, StringConstraints(strip_whitespace=True)] = Field(
        ..., title="请求路径"
    )
    method: Annotated[str, StringConstraints(strip_whitespace=True)] = Field(
        ..., title="method"
    )
    ip: Annotated[str, StringConstraints(strip_whitespace=True)] = Field("", title="ip")
    url: Annotated[str, StringConstraints(strip_whitespace=True)] = Field(
        "", title="完整地址"
    )
    headers: Annotated[List[list], Field()] = Field([], title="请求头")
    query_params: dict = Field({}, title="请求参数")
    path_params: dict = Field({}, title="路径参数")
    body: Annotated[str, StringConstraints(strip_whitespace=True)] = Field(
        "", title="请求体"
    )
    tags: Annotated[str, StringConstraints(strip_whitespace=True)] = Field(
        "", title="接口分类"
    )
    summary: Annotated[str, StringConstraints(strip_whitespace=True)] = Field(
        "", title="接口名称"
    )
    user_info: dict = Field({}, title="jwt用户信息")
    create_time: Annotated[str, StringConstraints(strip_whitespace=True)] = Field(
        "", title="创建时间"
    )

    @field_validator("create_time", mode="before")
    @classmethod
    def time_handler(cls, v, values, **kwargs):
        return vldtr_default_now_datetime()

    @field_validator("headers", mode="after")
    @classmethod
    def headers_handle(cls, v, values, **kwargs):
        new_headers = []
        # 过滤部分不需要的请求头信息
        for vv in v:
            if vv and vv[0] not in NEED_REMOVE_HEADERS:
                new_headers.append(vv)
        return new_headers


async def sys_access_log(
    request: Optional[Request] = None, slm: Optional[SysLogModel] = None
):
    """系统访问日志记录

    Args:
        request (Request): Request. Defaults to None.
        slm (SysLogModel): 日志模型, 部分接口没法复用 Request. Defaults to None.
    """
    if request and (not slm):
        _body = await get_request_body(request)
        # 获取真实的 ip (可能存在 nginx 等方式的代理)
        ip = [request.client.host]
        __x_forwarded_for = request.headers.getlist("X-Forwarded-For") or []
        __x_real_ip = request.headers.getlist("X-Real-Ip") or []
        if __x_forwarded_for:
            ip = __x_forwarded_for[0]
        elif __x_real_ip:
            ip = __x_real_ip

        api_info = (
            API_JSON.get()
            .get("paths", {})
            .get(request.url.path, {})
            .get(request.method.lower(), {})
        )
        slm = SysLogModel(
            uri=request.url.path,
            method=request.method,
            ip=",".join(ip),
            url=request.url.components.geturl(),
            headers=[[k, v] for k, v in request.headers.items()],
            query_params=request.query_params._dict,
            path_params=request.path_params,
            body="",
            tags=";".join(api_info.get("tags", [])),
            summary=api_info.get("summary", ""),
            user_info={},
            create_time="",
        )

        try:
            # 字符类参数可以进行编码存储
            slm.body = _body.decode()
        except Exception as e:
            logger.error(e)
            slm.body = f"** It could be a byte file ({e}) **"

        # 获取用户 JWT 中的信息
        auth_str = request.headers.get("Authorization") or ""
        _, jwt = get_authorization_scheme_param(auth_str)
        if "/download" in slm.uri:
            jwt = slm.query_params.get("tk", "")
        if jwt:
            _, user_info = JWTAuth().decode_jwt(jwt, False)
            slm.user_info = user_info

    print(slm.model_dump_json())  # 若要记录日志可在此处进行持久化操作
