# -*- coding: utf-8 -*-
# @Time : 2021/8/30 11:20
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : urls.py
# @Software: PyCharm
from django.urls import re_path
from rest_framework import routers

from . import views

# 自动注册路由
router = routers.SimpleRouter()
# router.register('user', views.UserViewSet)
router.register('post', views.PostViewSet)
router.register('role', views.RoleViewSet)
router.register('dept', views.DeptViewSet)
router.register('menu', views.MenuViewSet)
router.register('button', views.ButtonViewSet)

router.register('user', views.customUserViewSet)
router.register('user_face', views.userFaceViewSet)
# router.register('permission', views.PermissionViewSet)
# namespace
# print(router.urls)
app_name = "rbac"
urlpatterns = [
    # re_path(r'^get_user_info/$', utils.LoginView.as_view()),
    # re_path(r'^users/$', views.UserAPIView.as_view()),
    # re_path(r'^users/(?P<pk>\d+)/$', views.UserAPIView.as_view()),
    re_path(r'^user/info/$', views.customUserViewSet.as_view({'get': 'get_user_info'})),
    re_path(r'^user/face/$', views.customUserViewSet.as_view({'get': 'get_faces'})),
    # re_path(r'^user_face/get_facesByID/$', views.customUserViewSet.as_view({'post': 'get_faces'})),
    re_path(r'^user_face/get_facesByID/$', views.userFaceViewSet.as_view({'post': 'get_facesByID'})),
    re_path('user/import/', views.customUserViewSet.as_view({'post': 'import_user'})),
    re_path('user/export/', views.customUserViewSet.as_view({'post': 'export_user'})),
    re_path('user/get_menus/', views.customUserViewSet.as_view({'get': 'get_menus'})),
    re_path('user/get_menu_button/', views.customUserViewSet.as_view({'get': 'get_menu_button'})),
    re_path('post/test/', views.PostViewSet.as_view({'get': 'test'})),
    re_path('dept/get_dept_tree/', views.DeptViewSet.as_view({'get': 'get_dept_tree'})),
    re_path('button/get_buttonByMenuID/', views.ButtonViewSet.as_view({'post': 'get_buttonByMenuID'})),
    re_path('role/get_Menu_Button_ByRoleID/', views.RoleViewSet.as_view({'post': 'get_Menu_Button_ByRoleID'})),
    re_path('menu/get_Menu_Button/', views.MenuViewSet.as_view({'get': 'get_Menu_Button'})),
]
urlpatterns += router.urls
