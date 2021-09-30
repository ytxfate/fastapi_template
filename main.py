#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  main.py  
@Desc :  启动
'''

# Standard library imports
# Third party imports
import uvicorn
# Local application imports
from project.config.sys_config import app_run_conf, isFormalSystem
from project.config.log_config import CUSTOM_LOGGING_CONFIG


def main_run():
    if isFormalSystem is True:
        app_run_conf['RELOAD'] = False
        app_run_conf['DEBUG'] = False
    uvicorn.run("project.app:app",
                host=app_run_conf['HOST'],
                port=app_run_conf['PORT'],
                reload=app_run_conf['RELOAD'],
                workers=app_run_conf['WORKERS'],
                debug=app_run_conf['DEBUG'],
                log_config=CUSTOM_LOGGING_CONFIG)


if __name__ == "__main__":
    main_run()
