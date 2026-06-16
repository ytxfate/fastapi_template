#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  info.py
@Desc :  测试信息
"""

import csv
import io
import time
from urllib.parse import quote

from fastapi import APIRouter, Depends, File, Security, UploadFile
from fastapi.requests import Request
from fastapi.responses import Response, StreamingResponse
from openpyxl import Workbook

from project.dependencies.auth_depend import check_jwt
from project.dependencies.download_depend import check_download_jwt
from project.models.auth_models import JWTBodyInfo
from project.utils.api_limiter import api_user_limiter
from project.utils.comm_ret import comm_ret
from project.utils.operate_redis import OperateRedis
from project.utils.opt_redis_sentinel import OptRedisSentinel

info_router = APIRouter()
redis_m, redis_s = OptRedisSentinel().conn_redis()


# ----------------------------- 权限控制 -------------------------------------- #
@info_router.get("/dep_security_1")
def dep_security_1(jwtbi: JWTBodyInfo = Security(check_jwt, scopes=["info1"])):
    return comm_ret(resp=jwtbi.dict())


@info_router.get("/dep_security_2")
def dep_security_2(jwtbi: JWTBodyInfo = Security(check_jwt, scopes=["info2"])):
    return comm_ret(resp=jwtbi.dict())


# ------------------------------- 下载 --------------------------------------- #
@info_router.get("/download_csv_use_IO")
def download_csv_use_IO():
    csv_data = [
        ["name", "sex", "birthday"],
        ["user", "boy", "2019-01-01"],
        ["张三", "里斯", "2019-01-01"],
    ]
    # 创建一个 io 流
    io_stream = io.StringIO()
    writer = csv.writer(io_stream)
    for row in csv_data:
        writer.writerow(row)
    mem = io.BytesIO()
    mem.write(io_stream.getvalue().encode("utf-8"))
    # Change stream position
    mem.seek(0)
    io_stream.close()
    return Response(
        mem.read(),
        media_type="text/csv",
        headers={
            "content-disposition": "attachment; filename*=utf-8''{}".format(
                quote("测试.csv")
            )
        },
    )


async def download(csv_data):
    for v in csv_data:
        yield (",".join(v) + "\n").encode("utf-8")


@info_router.get("/download_csv_use_generator")
def download_csv_use_generator():
    csv_data = [
        ["name", "sex", "birthday"],
        ["ttt", "ttt", "2019-01-01"],
        ["TTT", "TTT", "2019-01-01"],
    ]
    return StreamingResponse(
        download(csv_data),
        media_type="text/csv",
        headers={
            "content-disposition": "attachment; filename*=utf-8''{}".format(
                quote("测试.csv")
            )
        },
    )


@info_router.get("/download_excel_use_IO")
async def download_excel_use_IO(
    jwtbi: JWTBodyInfo = Security(check_download_jwt, scopes=["info1"])
):
    wb = Workbook()
    ws = wb.active
    ws.title = "记录"

    headers = ["标题1", "标题2", "标题3", "标题4", "标题5"]
    ws.append(headers)

    sio = io.BytesIO()
    wb.save(sio)
    sio.seek(0)  # 重置指针

    return Response(
        sio.read(),
        media_type="application/vnd.ms-excel",
        headers={
            "Content-Disposition": f'attachment; filename*=utf-8\'\'{quote("测试.xlsx")}',
        },
    )


@info_router.post("/upload")
def test_upload(f: UploadFile = File(...)):
    return comm_ret(resp={"name": f.filename})


# ------------------------------ 数据库操作 ----------------------------------- #
@info_router.get("/opt_redis_sentinel")
def opt_redis_sentinel():
    print(id(redis_m), id(redis_s))
    t_now = str(int(time.time() * 1000))
    print(redis_m.hset("test", t_now, t_now))
    print(redis_s.hget("test", t_now))
    return comm_ret(resp=t_now)


@info_router.get("/opt_redis")
def opt_redis():
    red = OperateRedis()
    print(id(red))
    redis_cli = red.conn_redis()
    # print(redis_cli.hget("test", "test"))
    print(id(redis_cli))
    return comm_ret()


@info_router.get("/limiter1")
@api_user_limiter.limit("1/5second")
def limiter1(
    request: Request,
):
    return comm_ret(resp={"limiter1": "limiter1"})


@info_router.get("/limiter2")
@api_user_limiter.limit(
    "1/5second"
)  # [count] [per|/] [n (optional)] [second|minute|hour|day|month|year]
def limiter2(request: Request, jwt_info: JWTBodyInfo = Depends(check_jwt)):
    return comm_ret(resp={"limiter2": "limiter2", "jwt_info": jwt_info.dict()})
