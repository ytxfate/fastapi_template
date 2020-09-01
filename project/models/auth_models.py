#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  auth_models.py  
@Desc :  认证
'''

# Standard library imports

# Third party imports
from pydantic import constr, conlist
# Local application imports
from project.models.proj_base_model import ProjectBaseModel


class JWTBodyInfo(ProjectBaseModel):
    """jwt 中存储的信息
    """
    username: constr(strip_whitespace=True, min_length=1)
    scopes: conlist(constr(strip_whitespace=True))=[]
