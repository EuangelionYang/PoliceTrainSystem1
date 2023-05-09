# -*- coding: utf-8 -*-
# @Time : 2021/8/30 18:47
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : utils.py.py
# @Software: PyCharm
import base64
import io
from collections import OrderedDict

import numpy as np
from PIL import Image
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView

from face_rec.compare import compare
from utils.response import APIResponse
from .models import User
from .serializers import userSerializer


class LoginSerializer(TokenObtainPairSerializer):
    """
    两种方式登录：1.用户名密码 2.face_recognition
    """

    def validate(self, attrs):

        username = attrs['username']
        password = attrs['password']

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            data = super().validate(attrs)
            refresh = self.get_token(user)
            data['id'] = self.user.id
            data['username'] = self.user.username
            data['last_login'] = self.user.last_login
            resp = {
                'code': 200,
                'data': data,
                'msg': '登录成功'
            }
        else:
            resp = {
                'code': 400,
                'data': None,
                'msg': '登录失败，用户名或密码错误！'
            }
        return resp


# 登录视图
# @swagger_auto_schema(
#     responses={
#         '200': openapi.Response('获取成功')
#     },
#     security=[],
#     operation_id='captcha-get',
#     operation_description='获取用户信息',
# )
@method_decorator(name='post',
                  decorator=swagger_auto_schema(
                      operation_summary='用户登录',
                      operation_description='用户登录接口',
                      responses={status.HTTP_200_OK: openapi.Schema(
                          type=openapi.TYPE_OBJECT,
                          properties={"code": openapi.Schema(type=openapi.TYPE_NUMBER),
                                      "data": openapi.Schema(type=openapi.TYPE_OBJECT),
                                      "msg": openapi.Schema(type=openapi.TYPE_STRING)
                                      },
                          default={
                              "code": 200,
                              "data": {
                                  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzNzMwNzE5MSwianRpIjoiOThhYjExYjFlNTcxNDFmN2JkOGExZjk4ODE1NTJjNTAiLCJ1c2VybmFtZSI6Inlhbmd5dSJ9.ZKor-UrfWxxPx2nEIA3GNV6Xtad3giLJTpMFPq9Rusc",
                                  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM3MzA3MTkxLCJqdGkiOiI3YmU5MTRkODBkNTc0YzMyOTU3MDlkYzdjN2E5OGI4NiIsInVzZXJuYW1lIjoieWFuZ3l1In0.8tndl_3p_ytdX_zssJI2v1DcAdbSCk1CEgZPHha0I0w",
                                  "id": 1,
                                  "username": "yangyu",
                                  "last_login": "2021-10-23T14:51:06.222534"
                              },
                              "msg": "登录成功"
                          }
                      ),
                          status.HTTP_400_BAD_REQUEST: openapi.Schema(
                              type=openapi.TYPE_OBJECT,
                              properties={
                                  "code": openapi.Schema(type=openapi.TYPE_NUMBER),
                                  "data": openapi.Schema(type=openapi.TYPE_STRING),
                                  "msg": openapi.Schema(type=openapi.TYPE_STRING),
                              },
                              default={
                                  "code": 400,
                                  "data": 'null',
                                  "msg": "登录失败，用户名或密码错误！"
                              }
                          )
                      }
                  ))
class LoginView(TokenObtainPairView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer


class FaceIDView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        base64_str = request.data['face_base64']
        base64_str = base64_str.replace(' ', '+')
        img_b64decode = base64.b64decode(base64_str.split('base64,')[1])
        img = io.BytesIO(img_b64decode)
        to_check_img = np.asarray(Image.open(img))

        user = compare(to_check_img)
        if user:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            data = {}
            data['id'] = user.id
            data['username'] = user.username
            data['last_login'] = user.last_login
            data['access'] = str(access)
            data['refresh'] = str(refresh)
            resp = {
                'code': 200,
                'data': data,
                'msg': '登录成功'
            }
        else:
            resp = {
                'code': 100,
                'data': None,
                'msg': '登录失败，人脸无法匹配！'
            }
        return Response(resp)


class LogoutView(APIView):
    """
    用户注销接口
    """

    @swagger_auto_schema(operation_summary='注销登录',
                         operation_description='用户点击注销后，数据库中更新用户的last_login',
                         responses={status.HTTP_200_OK: openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 "code": openapi.TYPE_NUMBER,
                                 "msg": openapi.TYPE_STRING
                             },
                             default={
                                 "code": 200,
                                 "msg": "用户退出系统"
                             }

                         )})
    def get(self, request):
        resp = {
            'code': 200,
            'msg': '用户退出系统'
        }
        user = request.user
        # 修改上次登录时间为注销时间
        user.last_login = timezone.now()
        user.save()  # 这里记得保存一下
        return Response(resp)


# 重置密码视图
class resetPasswordView(APIView):
    """
    重置密码视图
    request={
    'id':user_id,
    'new_pwd':newpassword
    }
    """
    permission_classes = []

    def post(self, request):

        if request.user.is_staff:
            # 如果是超级管理员的话只需要传入id参数
            uid = request.data['id']
            new_password = request.data['new_pwd']
            user = User.objects.get(id=uid)
            user.set_password(new_password)
            user.save()
            return APIResponse(msg='重置密码成功')
        else:
            raise (PermissionError('您无权限重置密码！'))


class updatePasswordView(APIView):
    """
    更新密码视图,
    request={
    'old_pwd':old_password,
    'new_pwd':new_password
    }
    """

    def post(self, request):
        user = request.user
        old_pwd = request.data['old_pwd']
        new_pwd = request.data['new_pwd']
        if user.check_password(old_pwd):
            user.set_password(new_pwd)
            user.save()
            return APIResponse(code=200, msg='修改密码成功，请重新登录系统！')
        else:
            raise (ValueError('原密码错误，修改失败！'))


class CustomResponse():
    def __init__(self):
        self.status = 100
        self.msg = 'success'

    @property
    def get_dict(self):
        return self.__dict__
