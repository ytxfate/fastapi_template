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
from urllib.parse import quote
# Third party imports
from fastapi import APIRouter, Security, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
import xlwt
# Local application imports
from project.dependencies.auth_depend import check_jwt
from project.models.auth_models import JWTBodyInfo
from project.utils import resp_code
from project.utils.comm_ret import comm_ret
from project.utils.opt_redis_sentinel import OptRedisSentinel
from project.utils.operate_redis import OperateRedis


info_router = APIRouter()
redis_m, redis_s = OptRedisSentinel().conn_redis()

# ----------------------------- 权限控制 -------------------------------------- #
@info_router.get("/dep_security_1")
def dep_security_1(
    jwtbi: JWTBodyInfo=Security(check_jwt, scopes=['info1'])
):
    return comm_ret(resp=jwtbi.dict())


@info_router.get("/dep_security_2")
def dep_security_2(
    jwtbi: JWTBodyInfo=Security(check_jwt, scopes=['info2'])
):
    return comm_ret(resp=jwtbi.dict())


# ------------------------------- 下载 --------------------------------------- #
@info_router.get("/download_csv_use_IO")
def download_csv_use_IO():
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


async def download(csv_data):
    for v in csv_data:
        yield (",".join(v) + '\n').encode("utf-8")


@info_router.get("/download_csv_use_generator")
def download_csv_use_generator():
    csv_data = [
        ['name', 'sex', 'birthday'],
        ['ttt', 'ttt', '2019-01-01'],
        ['TTT', 'TTT', '2019-01-01']
    ]
    return StreamingResponse(
        download(csv_data), media_type="text/csv",
        headers={
            'content-disposition': "attachment; filename*=utf-8''{}".format(
                quote("测试.csv"))
    })


@info_router.get("/download_excel_use_IO")
def download_excel_use_IO(
    tk: str
):
    sio = io.BytesIO()
    wb = xlwt.Workbook()
    wb.encoding="utf-8"
    ws = wb.add_sheet("记录")
    for x, h in enumerate(['标题1','标题2','标题3','标题4','标题5']):
        ws.write(0, x, h)
    wb.save(sio)
    sio.seek(0)
    return StreamingResponse(
        sio, media_type="application/vnd.ms-excel",
        headers={
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': 'attachment; filename=' + quote("测试.xls")
        }
    )

@info_router.post("/upload")
def test_upload(f: UploadFile=File(...)):
    return comm_ret(resp={'name': f.filename})
    

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
