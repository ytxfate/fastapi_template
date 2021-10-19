#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  handle_regexp.py  
@Desc :  正则支持
'''

# Standard library imports
import re
# Third party imports
# Local application imports


NEED_EXCHG_CHAR = ['.', '^', '$', '*', '+', '?', '\\', '[', ']', '|',
                   '{', '}', '(', ')']

def handle_regexp(val: str):
    """正则转义
    """
    for c in NEED_EXCHG_CHAR:
        if c in val:
            val = val.replace(c, '\\' + c)
    return val

if __name__ == "__main__":
    print(re.search(handle_regexp('(对\私)'), "贷(对\私)"))
    print(re.search(handle_regexp('(对\私)'), "贷对\私"))
