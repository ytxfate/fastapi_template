#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  info.py  
@Desc :  测试信息
'''

# Standard library imports
import csv
import io
import time
# Third party imports
from fastapi import APIRouter, Security
from fastapi.responses import StreamingResponse, FileResponse
from urllib.parse import quote
# Local application imports
from project.dependencies.auth_depend import check_jwt
from project.models.auth_models import JWTBodyInfo
from project.utils import resp_code
from project.utils.comm_ret import comm_ret
from project.utils.opt_redis_sentinel import OptRedisSentinel
from project.utils.operate_redis import OperateRedis


info_router = APIRouter()
redis_m, redis_s = OptRedisSentinel().conn_redis()

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

@info_router.get("/info3")
def info3():
    csv_data = [
        ['name', 'sex', 'birthday'],
        ['user', 'boy', '2019-01-01'],
        ['张三', '里斯', '2019-01-01']
    ]
    # 创建一个 io 流
    io_stream = io.StringIO()
    writer = csv.writer(io_stream)
    for row in csv_data:
        writer.writerow(row)
    mem = io.BytesIO()
    mem.write(io_stream.getvalue().encode('utf-8'))
    # Change stream position
    mem.seek(0)
    io_stream.close()
    return StreamingResponse(
        mem, media_type="text/csv",
        headers={
            'content-disposition': "attachment; filename*=utf-8''{}".format(
                quote("测试.csv"))
    })


@info_router.get("/info4")
def info4():
    print(id(redis_m), id(redis_s))
    t_now = str(int(time.time() * 1000))
    print(redis_m.hset("test", t_now, t_now))
    print(redis_s.hget("test", t_now))
    return comm_ret(resp=t_now)


@info_router.get("/info5")
def info5():
    red = OperateRedis()
    print(id(red))
    redis_cli = red.conn_redis()
    # print(redis_cli.hget("test", "test"))
    print(id(redis_cli))
    return comm_ret()
