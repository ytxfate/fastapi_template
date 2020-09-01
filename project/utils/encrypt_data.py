#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  encrypt_data.py  
@Desc :  数据加密
'''

# Standard library imports
from typing import Union
import hashlib
# Third party imports

# Local application imports


class EncrypData:
    """MD5 及 HASH 加密
    """
    def __init__(self, encrypt_data: Union[str, bytes]):
        if not isinstance(encrypt_data, (str, bytes)):
            raise TypeError("The encrypted data type is not supported")
        # str to bytes
        if isinstance(encrypt_data, str):
            encrypt_data = encrypt_data.encode("utf-8")

        self.encrypt_data = encrypt_data


    def encrypt_md5(self) -> str:
        """md5 加密  
        @return:
            返回一个32位加密后的字符串
        """
        m = hashlib.md5()
        m.update(self.encrypt_data)
        return m.hexdigest()

    def encrypt_sha1(self) -> str:
        """hash 加密  
        @return:
            返回一个40位加密后的字符串
        """
        h = hashlib.sha1()
        h.update(self.encrypt_data)
        return h.hexdigest()

    def encrypt_sha224(self) -> str:
        """hash 加密  
        @return:
            返回一个56位加密后的字符串
        """
        h = hashlib.sha224()
        h.update(self.encrypt_data)
        return h.hexdigest()

    def encrypt_sha256(self) -> str:
        """hash 加密  
        @return:
            返回一个64位加密后的字符串
        """
        h = hashlib.sha256()
        h.update(self.encrypt_data)
        return h.hexdigest()

    def encrypt_sha384(self) -> str:
        """hash 加密  
        @return:
            返回一个96位加密后的字符串
        """
        h = hashlib.sha384()
        h.update(self.encrypt_data)
        return h.hexdigest()

    def encrypt_sha512(self) -> str:
        """hash 加密  
        @return:
            返回一个128位加密后的字符串
        """
        h = hashlib.sha512()
        h.update(self.encrypt_data)
        return h.hexdigest()
