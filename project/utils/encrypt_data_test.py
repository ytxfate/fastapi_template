#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  encrypt_data_test.py
@Desc :  数据加密测试案例
"""

from project.utils.encrypt_data import EncrypData


class TestEncrypData:
    def test_md5(self):
        assert EncrypData("123").encrypt_md5() == "202cb962ac59075b964b07152d234b70"

    def test_sha1(self):
        assert (
            EncrypData("123").encrypt_sha1()
            == "40bd001563085fc35165329ea1ff5c5ecbdbbeef"
        )

    def test_sha224(self):
        assert (
            EncrypData("123").encrypt_sha224()
            == "78d8045d684abd2eece923758f3cd781489df3a48e1278982466017f"
        )

    def test_sha256(self):
        assert (
            EncrypData("123").encrypt_sha256()
            == "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
        )

    def test_sha384(self):
        assert (
            EncrypData("123").encrypt_sha384()
            == "9a0a82f0c0cf31470d7affede3406cc9aa8410671520b727044eda15b4c25532a9b5cd8aaf9cec4919d76255b6bfb00f"
        )

    def test_sha512(self):
        assert (
            EncrypData("123").encrypt_sha512()
            == "3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2"
        )
