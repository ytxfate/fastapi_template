#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  jwt_auth.py  
@Desc :  JWT 编码、解码
'''

# Standard library imports
from typing import Union, Tuple
import datetime
import hashlib
import logging
import time
# Third party imports
import jwt
# Local application imports
from project.config.sys_config import SECRET_KEY as jwt_secret_key
from project.utils.encrypt_data import EncrypData


logger = logging.getLogger(__name__)

class JWTAuth:
    """
    JSON Web Token 用户认证
    """
    VALIDITY_PERIOD = 30
    def __init__(self):
        self.secret_key = EncrypData(jwt_secret_key).encrypt_md5()


    def __encode_jwt(self,
                    data: dict,
                    validity_period: int=VALIDITY_PERIOD) -> Tuple[bool, str]:
        """
        生成 jwt 认证信息
            @param:
                data: jwt 需要存储数据
                validity_period: jwt 有效期，默认 30 分钟
            @return:
                加密是否成功
                jwt 字串
        """
        try:
            payload = {
                'exp': time.mktime((
                        datetime.datetime.now() +
                        datetime.timedelta(minutes=validity_period)
                    ).timetuple()),    # 过期时间
                'iat': time.mktime(
                    datetime.datetime.now().timetuple()), # 发行时间
                'iss': 'hsd',   # token签发者
                'data': data
            }
            jwt_body = jwt.encode(
                payload,
                self.secret_key,
                algorithm='HS256'
            )
            return True, jwt_body
        except Exception as e:
            logger.exception(e)
        return False, ""


    def decode_jwt(self,
                    jwt_str: str,
                    verify_exp: bool=True) -> Tuple[bool, dict]:
        """
        解析 jwt 认证信息
            @param:
                jwt_body: jwt 字串
                verify_exp: 是否验证 jwt 时效性
            @return:
                解析状态 及 jwt 字串中的用户信息
                当 解析状态 为 True 时，解析成功；否则解析失败            
        """
        options={'verify_exp': verify_exp}
        try:
            jwt_payload = jwt.decode(
                jwt_str,
                self.secret_key,
                algorithms=['HS256'],
                options=options
            )
            if jwt_payload and 'data' in jwt_payload:
                return True, jwt_payload['data']
        except Exception as e:
            logger.error(e)
                
        return False, {}


    def decode_jwt_check_refresh_jwt(self,
                                    jwt_str: str,
                                    refresh_jwt_str: str) -> Tuple[bool, dict]:
        """解析 jwt 及 refresh_jwt 认证信息
        """
        jwt_stat, data = self.decode_jwt(jwt_str, False)
        if jwt_stat is False:
            return False, {}
        re_jwt_stat, re_data = self.decode_jwt(refresh_jwt_str, True)
        if re_jwt_stat is False:
            return False, {}
        # 检验 jwt 与 refresh_jwt 是否匹配
        sha_jwt_str = EncrypData(jwt_str).encrypt_sha256()
        if sha_jwt_str == re_data.get("v"):
            return True, data
        return False, {}

    def create_jwt_and_refresh_jwt(self, data: object,
                validity_period: str=VALIDITY_PERIOD) -> Tuple[bool, str, str]:
        """
        生成 jwt 及 refresh_jwt 信息
            @param:
                data: jwt 需要存储数据
                validity_period: jwt 有效期，默认 30 分钟
            @return:
                create_status jwt 生成状态
                jwt 字串
                refresh_jwt 字串
        """
        jwt = refresh_jwt = ""
        # 最多循环 5 次，否则生成失败
        # 生成 jwt
        for _ in range(5):
            jwt_stat, jwt = self.__encode_jwt(data,
                                                validity_period=validity_period)
            if jwt_stat is True:
                break
            else:
                continue
        else:
            return False, "", ""

        refresh_data = EncrypData(jwt).encrypt_sha256()
        for _ in range(5):
            re_jwt_stat, refresh_jwt = self.__encode_jwt(
                {"v": refresh_data},
                validity_period=validity_period*2
            )
            if re_jwt_stat is True:
                return True, jwt, refresh_jwt
            else:
                continue
        else:
            return False, "", ""
