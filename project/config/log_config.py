#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  log_config.py  
@Desc :  日志配置
'''

# Standard library imports
from copy import deepcopy
import logging
# Third party imports
from uvicorn.config import LOGGING_CONFIG
# Local application imports
from .sys_config import isFormalSystem



__cus_log_conf = deepcopy(LOGGING_CONFIG)
__cus_log_conf['formatters']['default']['fmt'] = "%(asctime)s - %(levelprefix)s %(name)s:%(filename)s:%(lineno)-5d - %(message)s"
# __cus_log_conf['formatters']['default']['fmt'] = '%(asctime)s - ' + __cus_log_conf['formatters']['default']['fmt']
__cus_log_conf['formatters']['access']['fmt'] = '%(asctime)s - %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'  # noqa: E501
# __cus_log_conf['formatters']['access']['fmt'] = '%(asctime)s - ' + __cus_log_conf['formatters']['access']['fmt']
__cus_log_conf['loggers']['uvicorn'] = {"handlers": ["default"], "level": logging.DEBUG}
if isFormalSystem is True:
    __cus_log_conf['loggers']['uvicorn'] = {"handlers": ["default"], "level": "INFO"}

CUSTOM_LOGGING_CONFIG = __cus_log_conf
