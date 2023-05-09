# -*- coding: utf-8 -*-
# @Time : 2021/9/13 16:30
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : response.py
# @Software: PyCharm
from rest_framework.response import Response


# 自定义response
class APIResponse(Response):
    def __init__(self, code=200, msg='成功', status=None, headers=None, **kwargs):
        dic = {'code': code,
               'msg': msg,
               }
        dic.update(kwargs)
        super().__init__(data=dic, status=status, headers=headers)
