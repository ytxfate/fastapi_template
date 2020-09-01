#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  handle_req_param.py  
@Desc :  检查及处理 request 请求参数
'''

# Standard library imports
import re
# Third party imports

# Local application imports


class HandleReqParam:
    """
    检查及处理 request 请求参数
        @param:
            request_dict :  request 请求的参数及值
    """
    def __init__(self, request_dict: dict):
        self.request_dict = request_dict
    
    def __remove_spaces(self):
        """
        去除 str 首尾的空格
        """
        for key, val in self.request_dict.items():
            if isinstance(val, str):
                self.request_dict[key] = val.strip()

    def __check_required_keys(self, must_need_keys: list):
        """
        检查必要参数是否不全或为空
            @param:
                must_need_keys  : api 接口函数必要的 request 参数
            @retuen:
                return Boolean
                if return is False,the parameters is check fail,
                if return is True,the parameters is check success
        """
        for must_key in must_need_keys:
            if must_key not in self.request_dict:
                return False
            # 参数类型为字符串时，值不能为空字符串
            if isinstance(self.request_dict[must_key], str):
                if self.request_dict[must_key].strip() == '':
                    return False
            else:
                if self.request_dict[must_key] is None:
                    return False
        return True

    def __check_param_can_change_keys(self, can_change_keys: list):
        """
        检查请求的所有参数是否都在允许修改的 keys 中
            @param:
                can_change_keys : api 接口函数允许的 request 参数
            @retuen:
                return Boolean
                if return is False,the parameters is check fail,
                if return is True,the parameters is check success
        """
        for key in self.request_dict.keys():
            if key not in can_change_keys:
                return False
        return True

    def __support_regex_choose(self, need_regexp_keys: list):
        """
        对部分需要进行模糊匹配的字段进行处理
            @param:
                need_regexp_keys : 需要模糊查询的参数集
        """
        for key, value in self.request_dict.items():
            if key in need_regexp_keys:
                self.request_dict[key] = re.compile(value)
    
    def main_contraller(self, rm_spaces: bool=True, required_keys: list=[],
                            allow_keys: list=[], regexp_keys: list=[]):
        """
        主控制器
            @param:
                rm_spaces       :  是否去除 str 首尾的空格
                required_keys   :  检查必要参数是否不全或为空
                allow_keys      :  检查请求的所有参数是否都在允许修改的 keys 中
                regexp_keys     :  对部分需要进行模糊匹配的字段进行处理
            @return: tuple(check_status, request_dict)
                check_status     : 必要参数 及 允许修改参数 检查结果
                                    if return is False,the parameters is check fail,
                                    if return is True,the parameters is check success
                request_dict     : 处理后的参数
        """
        # request_dict 为空时直接返回 False
        if not self.request_dict:
            return (False, self.request_dict)
        # request_dict 类型不对的直接返回 False
        if not isinstance(self.request_dict, dict):
            return False, self.request_dict
        check_status_imp = False
        check_status_can = False
        check_status = False
        # 去空
        if rm_spaces:
            self.__remove_spaces()
        # 检查必要参数是否不全或为空
        if required_keys:
            check_status_imp = self.__check_required_keys(required_keys)
        if allow_keys:
            check_status_can = self.__check_param_can_change_keys(allow_keys)
        if regexp_keys:
            self.__support_regex_choose(regexp_keys)
        # 判断检查的结果
        if ((bool(required_keys) is check_status_imp) and
                    (bool(allow_keys) is check_status_can)):
            check_status = True
        return (check_status, self.request_dict)
