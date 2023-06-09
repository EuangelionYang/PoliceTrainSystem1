# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/6 006 10:30
@Remark: 自定义权限
"""
import re

from rest_framework.permissions import BasePermission

from rbac.models import MenuButton


def ValidationApi(reqApi, validApi):
    """
    验证当前用户是否有接口权限
    :param reqApi: 当前请求的接口
    :param validApi: 用于验证的接口
    :return: True或者False
    """
    if validApi is not None:
        valid_api = validApi.replace('{id}', '.*?')
        matchObj = re.match(valid_api, reqApi, re.M | re.I)
        if matchObj:
            return True
        else:
            return False
    else:
        return False


class CustomPermission(BasePermission):
    """自定义权限"""

    def has_permission(self, request, view):

        # 对ViewSet下的def方法进行权限判断
        # 当权限为空时,则可以访问
        is_head = getattr(view, 'head', None)
        # print(view.permission_classes)
        if is_head:
            head_kwargs = getattr(view.head, 'kwargs', None)
            if head_kwargs:
                _permission_classes = getattr(head_kwargs, 'permission_classes', None)
                if _permission_classes is None:
                    return True

        # 判断是否是超级管理员

        if request.user.is_admin:
            return True
        else:
            api = request.path  # 当前请求接口
            # print("api---------------", api)
            is_permission = MenuButton.objects.filter(api=api).exists()
            if not is_permission:
                print(api)
                return True
            method = request.method  # 当前请求方法
            # print("method------------", method)
            methodList = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
            method = methodList.index(method)
            if not hasattr(request.user, "role"):
                return False
            # 获取用户的ApiList
            userApiList = request.user.role.values('permissions__api', 'permissions__method')  # 获取当前用户的角色拥有的所有接口
            for item in userApiList:
                valid = ValidationApi(api, item.get('permissions__api'))
                if valid and (method == item.get('permissions__method')):
                    return True
        return False
