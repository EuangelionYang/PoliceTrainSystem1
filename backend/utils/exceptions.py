# -*- coding: utf-8 -*-
# @Time : 2021/9/13 14:56
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : exceptions.py
# @Software: PyCharm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


# 自定义异常处理方法
def custom_exception_handler(exc, context):
    resp = exception_handler(exc, context)
    if not resp:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'code': 400, 'msg': str(exc)})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'code': 400, 'msg': resp.data})
