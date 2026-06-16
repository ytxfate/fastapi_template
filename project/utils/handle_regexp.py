#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File :  handle_regexp.py
@Desc :  正则支持
"""

import re

NEED_EXCHG_CHAR = [
    "\\",
    ".",
    "^",
    "$",
    "*",
    "+",
    "?",
    "[",
    "]",
    "|",
    "{",
    "}",
    "(",
    ")",
]


def handle_regexp(val: str):
    """正则转义"""
    for c in NEED_EXCHG_CHAR:
        if c in val:
            val = val.replace(c, "\\" + c)
    return val


if __name__ == "__main__":
    print(re.search(handle_regexp(r"(对\私)"), r"贷(对\私)"))
    print(re.search(handle_regexp(r"(对\私)"), r"贷对\私"))
