#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  jwt_auth.py
@Desc :  JWT 编码、解码
'''

# The Python Standard Modules(Library) and Third Modules(Library)
import datetime
import time
import jwt
import hashlib
import logging
from typing import Union, Tuple
# User-defined Modules
from project.config.sys_config import SECRET_KEY as jwt_secret_key

logger = logging.getLogger(__name__)

class JWTAuth:
    """
    JSON Web Token 用户认证
    """
    VALIDITY_PERIOD = 30
    def __init__(self):
        self.secret_key = self.encrypt_md5(jwt_secret_key)

    def encrypt_md5(self, encrypt_str: Union[str, bytes]) -> str:
        """
        md5 加密
            @param:
                encrypt_str: 需要加密的字符串(str)或字节码(bytes)
            @return:
                返回一个32位加密后的字符串
        """
        if isinstance(encrypt_str, str):
            # 如果是 unicode 先转 utf-8
            encrypt_str = encrypt_str.encode("utf-8")
        m = hashlib.md5()
        m.update(encrypt_str)
        return m.hexdigest()

    def __encode_jwt(self, user_info: object,
                validity_period: int=VALIDITY_PERIOD) -> str:
        """
        生成 jwt 认证信息
            @param:
                user_info: jwt 需要存储数据
                validity_period: jwt 有效期，默认 30 分钟
            @return:
                jwt 字串
        """
        jwt_body = None
        try:
            payload = {
                'exp': time.mktime((
                        datetime.datetime.now() +
                        datetime.timedelta(minutes=validity_period)
                    ).timetuple()),    # 过期时间
                'iat': time.mktime(
                    datetime.datetime.now().timetuple()), # 发行时间
                'iss': 'hsd',   # token签发者
                'data': user_info
            }
            jwt_body = jwt.encode(
                payload,
                self.secret_key,
                algorithm='HS256'
            ).decode(encoding='utf-8')
        except Exception as e:
            logger.exception(e)
        return jwt_body
    
    def decode_jwt(self, jwt_body: str) -> Tuple[bool, object]:
        """
        解析 jwt 认证信息
            @param:
                jwt_body: jwt 字串
            @return:
                解析状态 及 jwt 字串中的用户信息
                当 解析状态 为 True 时，解析成功；否则解析失败            
        """
        user_info = {}
        decode_status = False
        try:
            jwt_payload = jwt.decode(
                jwt_body.encode(encoding='utf-8'),
                self.secret_key,
                options={'verify_exp': True}
            )
            if jwt_payload and 'data' in jwt_payload:
                user_info = jwt_payload['data']
                decode_status = True
        except Exception as e:
            logger.exception(e)
        return decode_status, user_info
    
    def decode_jwt_without_check(self, jwt_body: str) -> object:
        """
        解析 jwt 认证信息，不验证 jwt_body 时效性
            @param:
                jwt_body: jwt 字串
            @return:
                返回解析的结果， 若返回 {} 则解析失败            
        """
        user_info = {}
        try:
            jwt_payload = jwt.decode(
                jwt_body.encode(encoding='utf-8'),
                self.secret_key,
                options={'verify_exp': False}
            )
            if jwt_payload and 'data' in jwt_payload:
                user_info = jwt_payload['data']
        except Exception as e:
            logger.exception(e)
        return user_info
    
    def create_jwt_and_refresh_jwt(self, user_info: object,
                validity_period: str=VALIDITY_PERIOD) -> Tuple[bool, str, str]:
        """
        生成 jwt 及 refresh_jwt 信息
            @param:
                user_info: jwt 需要存储数据
                validity_period: jwt 有效期，默认 30 分钟
            @return:
                create_status jwt 生成状态
                jwt 字串
                refresh_jwt 字串
        """
        jwt = refresh_jwt = None
        create_status = False
        # 最多循环 5 次，否则生成失败
        for _ in range(5):
            jwt = self.__encode_jwt(user_info,validity_period=validity_period)
            refresh_jwt = self.__encode_jwt(
                {}, validity_period=validity_period*2)
            if jwt and refresh_jwt:
                create_status = True
                break
        return create_status, jwt, refresh_jwt
