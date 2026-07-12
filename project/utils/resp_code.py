#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  resp_code.py
@Desc :  自定义 response code
"""

RespCode = int
# ===================  基本 HTTP response code  =================== #
SUCCESS: RespCode = 200  # 成功
EXCEPTION_ERROR: RespCode = 400  # 异常错误

# ===================  其他 HTTP response code  =================== #
PARAMETER_ERROR: RespCode = 1000  # 参数异常错误
DATA_CHECK_ERROR: RespCode = 1001  # 数据比对出错(数据库中不存在或已存在此数据)
DATA_INSERT_ERROR: RespCode = 1002  # 数据写入数据库出错
DATA_UPDATE_ERROR: RespCode = 1003  # 数据库数据更新出错
DATA_DELETE_ERROR: RespCode = 1004  # 数据库数据删除出错
DOCUMENTS_ARE_NOT_SUPPORTED: RespCode = 1005  # 不支持的文件上传格式
FILE_NOT_FOUND: RespCode = 1006  # 文件不存在
DATA_CREATE_ERROR: RespCode = 1007  # 数据生成异常
# jwt 相关
JWT_CREATE_ERROR: RespCode = 1101  # jwt 生成异常
JWT_PARSE_ERROR: RespCode = 1102  # jwt 解析异常
# 用户相关
USER_NO_LOGIN: RespCode = 1200  # 用户未登录
USER_LOGOUT: RespCode = 1201  # 用户登出
USER_NO_ROLES: RespCode = 1202  # 用户没有角色
USER_NO_AUTHORITY: RespCode = 1203  # 用户没有此接口权限
# 接口相关
API_LIMIT: RespCode = 1300  # 接口限流
