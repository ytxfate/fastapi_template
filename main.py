#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  main.py  
@Desc :  启动
'''

# Standard library imports
from copy import deepcopy
# Third party imports
import uvicorn
from uvicorn.config import LOGGING_CONFIG
# Local application imports
from project.config.sys_config import app_run_conf, isFormalSystem



custom_logging_config = deepcopy(LOGGING_CONFIG)
custom_logging_config['formatters']['default']['fmt'] = '%(asctime)s - ' + custom_logging_config['formatters']['default']['fmt']
custom_logging_config['formatters']['access']['fmt'] = '%(asctime)s - ' + custom_logging_config['formatters']['access']['fmt']
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
                log_config=custom_logging_config)


if __name__ == "__main__":
    main_run()
