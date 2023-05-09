# -*- coding: utf-8 -*-
# @Time : 2021/8/27 15:12
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : serializers.py
# @Software: PyCharm
# from rest_framework.fields import CharField
from rest_framework import serializers
from utils.serializers import customModelSerializer
from rest_framework.serializers import (ModelSerializer, PrimaryKeyRelatedField,
                                        StringRelatedField, ListSerializer
                                        )
from rbac.models import *
from django.contrib.auth.hashers import make_password
from PoliceTrainSystem.settings import MEDIA_ROOT, BASE_DIR



class ButtonSerializer(customModelSerializer):
    class Meta:
        model = MenuButton
        fields = '__all__'


class MenuSerializer(customModelSerializer):
    parentId = PrimaryKeyRelatedField(source='parent',
                                      label='上级菜单', read_only=True)

    # parent = PrimaryKeyRelatedField(source='parent', write_only=True)

    class Meta:
        model = Menu
        # fields = '__all__'
        exclude = ['parent']


# class RolePermissionSerializer(customModelSerializer):
#     menu_list = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Role
#         fields = ['id', 'title', 'menu_list']
#         # fields = '__all__'
#
#     def get_menu_list(self, instance):
#         menus = instance.menus.all()
#         root_menus = menus.filter(parent=None)
#         print(menus)
#         buttons = instance.permissions.all()
#         menu_serializer = MenuTreeSerializer(instance=root_menus, many=True, context={'menus': menus})
#         menu_list = menu_serializer.data
#
#         # for each in menus:
#         #     menu = {}
#         #     menu['m_id'] = each.id
#         #     menu['m_title'] = each.title
#         #     menu['button_list'] = []
#         #     mb = each.button
#         #     for bt in buttons:
#         #         if mb.filter(id=bt.id).exists():
#         #             print('haha')
#         #             menu['button_list'].append({'b_id': bt.id,
#         #                                         'b_title': bt.title})
#         #     menu_list.append(menu)
#         return menu_list


class MenuButtonSerializer(customModelSerializer):
    class Meta:
        model = MenuButton
        fields = '__all__'


class PostSerializer(customModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class DeptSerializer(customModelSerializer):
    parentID = PrimaryKeyRelatedField(source='parent', queryset=Dept.objects.all(),
                                      label='上级部门ID', allow_null=True)
    parentTitle = StringRelatedField(source='parent', label='上级部门名称', read_only=True)

    class Meta:
        model = Dept
        fields = ['id', 'title', 'parentID', 'parentTitle', 'leader', 'telephone', 'sort', ]


class DeptTreeSerializer(customModelSerializer):
    children = serializers.SerializerMethodField()
    parentID = PrimaryKeyRelatedField(source='parent', queryset=Dept.objects.all(),
                                      label='上级部门ID', allow_null=True)
    parentTitle = StringRelatedField(source='parent', label='上级部门名称', read_only=True)

    class Meta:
        model = Dept
        fields = ['id', 'title', 'parentID', 'parentTitle',
                  'leader', 'telephone', 'sort', 'children']

    def get_children(self, instance):
        # depts:全部部门
        depts = self.context['depts']
        # children列表
        children = []
        temp = depts.filter(parent=instance).order_by('sort')

        for t in temp:
            item = DeptTreeSerializer(t, context={'depts': depts})
            children.append(item.data)
        return children


class RoleSerializer(customModelSerializer):
    """
    Role序列化器
    """

    class Meta:
        model = Role
        fields = '__all__'


class UserListSerializer(ListSerializer):
    # post请求调用的方法
    def create(self, validated_data):
        return super().create(validated_data)

    # put请求调用的方法
    def update(self, instance, validated_data):
        return [
            self.child.update(attrs, validated_data[i]) for i, attrs in enumerate(instance)
        ]


# class UserSerializer(ModelSerializer):
#     """
#     User序列化器
#     roles:一个用户可能对应多个角色
#     """
#     # 获取用户的所有权限，并将其序列化
#     # permissions = SerializerMethodField('get_user_permissions')
#     # required=True为反序列化必填
#     dept_name = serializers.CharField(source='dept.title', read_only=True)
#     post_name = serializers.CharField(source='post.title', read_only=True)
#     create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
#     role_list = StringRelatedField(source='role', many=True, read_only=True)
#
#     # create_time = serializers.DateTimeField(read_only=True)
#
#     # roles_list = serializers.SerializerMethodField('get_roles_list')
#
#     class Meta:
#         # many=True时使用UserListSerializer
#         list_serializer_class = UserListSerializer
#         model = User
#
#         # fields:序列化的字段
#         fields = ['id', 'username', 'name', 'dept_name', 'post_name',
#                   'gender', 'role', 'phone', 'email',
#                   'role_list', 'password', 'create_time', 'is_active', 'is_admin', 'avatar']
#         # read_only_fields = ['dept', 'post', 'roles']
#         extra_kwargs = {'password': {'write_only': True,
#                                      'required': True},
#                         'create_time': {'read_only': True}}
#
#     def validate_password(self, data):
#         # 密码长度大于6位
#         method = self.context['request'].method
#         if method.lower() == 'post':
#             # 创建用户时需要密码
#             if len(data) >= 6:
#                 # 将密码通过sha256加密后存到数据库中
#                 return make_password(data)
#             else:
#                 raise (ValueError('密码必须大于6位！'))

class userSerializer(customModelSerializer):
    """
    User序列化器
    roles:一个用户可能对应多个角色
    """
    # 获取用户的所有权限，并将其序列化
    # permissions = SerializerMethodField('get_user_permissions')
    # required=True为反序列化必填
    dept_name = serializers.CharField(source='dept', read_only=True)
    post_name = serializers.CharField(source='post', read_only=True)
    # create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    role_list = StringRelatedField(source='role', many=True, read_only=True)
    identifier_list = serializers.SerializerMethodField()

    # create_time = serializers.DateTimeField(read_only=True)

    # roles_list = serializers.SerializerMethodField('get_roles_list')
    def get_identifier_list(self, instance):
        roles = instance.role.all()
        res = []
        for each in roles:
            res.append(each.identifier)
        return res

    class Meta:
        # many=True时使用UserListSerializer
        list_serializer_class = UserListSerializer
        model = User

        # fields:序列化的字段
        fields = ['id', 'username', 'name', 'IDCard',
                  'gender', 'role', 'role_list', 'identifier_list',
                  'phone', 'email',
                  'dept', 'post', 'dept_name', 'post_name', 'password', 'is_active', 'is_admin', 'avatar', 'detail']
        # read_only_fields = ['dept', 'post', 'roles']
        extra_kwargs = {'password': {'write_only': True,
                                     'required': True},
                        'create_time': {'read_only': True}}

    # def validate_password(self, data):
    #     # 密码长度大于6位
    #     method = self.context['request'].method
    #     if method.lower() == 'post':
    #         # 创建用户时需要密码
    #         if len(data) >= 6:
    #             # 将密码通过sha256加密后存到数据库中
    #             return make_password(data)
    #         else:
    #             raise (ValueError('密码必须大于6位！'))


class userCreateSerializer(customModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name', 'password', 'IDCard', 'gender', 'role',
                  'dept', 'post',
                  'phone', 'email', 'is_active', 'avatar', 'detail']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, data):
        if len(data) >= 6:
            return make_password(data)
        else:
            raise (ValueError('密码不能长度小于6位'))


class userUpdateSerializer(customModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'role', 'IDCard', 'dept', 'post',
                  'phone', 'email', 'gender',
                  'is_active', 'avatar', 'detail']


class UserInfoSerializer(customModelSerializer):
    role_list = StringRelatedField(source='role', many=True, read_only=True)
    identifier_list = serializers.SerializerMethodField()
    # identifier_list = serializers.CharField(source='role.identifier', read_only=True)
    dept_name = serializers.CharField(source='dept', read_only=True)
    post_name = serializers.CharField(source='post', read_only=True)

    def get_identifier_list(self, instance):
        roles = instance.role.all()
        res = []
        for each in roles:
            res.append(each.identifier)
        return res

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'identifier_list',
                  'role_list', 'avatar', 'dept_name', 'post_name', 'dept', 'post']


class userFaceSerializer(customModelSerializer):
    uid = PrimaryKeyRelatedField(source='user', queryset=User.objects.all(), label='用户编号')

    class Meta:
        model = userFace
        fields = ['id', 'uid', 'face']


class retrieveUserFaceSerializer(customModelSerializer):
    class Meta:
        model = userFace
        fields = ['id', 'face']


class MenuTreeSerializer(serializers.Serializer):
    """
    返回菜单树，
    [{
        "path": "/permission",
        "component": "Layout",
        "meta": {
            "title": "permission",
            "icon": "el-icon-lock"
        },
        "name": "permission",
        "redirect": "/permission/users",
        "alwaysShow": true,
        children数组必须要是用户的目录列表
        "children": [
            {
                "path": "users",
                "name": "users",
                "component": "permission/user",
                "meta": {
                    "title": "users",
                    "icon": "el-icon-user"
                },
                "hidden": false
            }
        ]
        }]
    """
    id = serializers.SerializerMethodField()
    path = serializers.CharField(max_length=128, allow_null=True, allow_blank=True)
    name = serializers.CharField(max_length=128, allow_null=True, allow_blank=True)
    component = serializers.CharField(max_length=128, allow_null=True, allow_blank=True)
    meta = serializers.SerializerMethodField()
    redirect = serializers.CharField(max_length=128, allow_null=True, allow_blank=True)
    hidden = serializers.BooleanField()
    children = serializers.SerializerMethodField()

    def get_id(self, instance):
        return instance.id

    def get_meta(self, instance):
        return {
            'title': instance.title, 'icon': instance.icon}

    def get_children(self, instance):
        # menus:用户所有的菜单
        menus = self.context['menus']
        # children列表
        children = []
        temp = menus.filter(parent=instance).order_by('sort')

        for t in temp:
            item = MenuTreeSerializer(t, context={'menus': menus})
            children.append(item.data)
        return children


class PermissionTreeSerializer(customModelSerializer):
    """
    角色-菜单-权限树
    """

    menu_list = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'status', 'menu_list']

    def get_menu_list(self, instance):
        # menus:用户所有的菜单

        menus = instance.menus.all()
        root_menus = menus.filter(parent=None)
        buttons = instance.permissions.all()

        serializer = MenuButtonTreeSerializer(instance=root_menus, many=True, context={'role_menus': menus,
                                                                                       'role_buttons': buttons})
        return serializer.data


class RolePermissionTreeSerializer(customModelSerializer):
    """
    角色-菜单-权限树
    """

    menu_list = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'status', 'menu_list']

    def get_menu_list(self, instance):
        # menus:用户所有的菜单

        menus = instance.menus.all()
        root_menus = menus.filter(parent=None)
        buttons = instance.permissions.all()

        serializer = MenuButtonTreeSerializer(instance=root_menus, many=True, context={'role_menus': menus,
                                                                                       'role_buttons': buttons})
        return serializer.data


class MenuButtonTreeSerializer(customModelSerializer):
    """
    菜单-权限树
    [{
        "id":
        "name": "permission",
        "button_list":[]
        "children": [
            {
                "id":
                "name": "users",
                "button_list":[
                {}
                ]
            }
        ]
        }]
    """

    children = serializers.SerializerMethodField()
    button_list = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'title', 'children', 'button_list']

    def get_button_list(self, instance):
        role_buttons = self.context['role_buttons']
        button_list = []
        for each in role_buttons:
            if each.menu == instance:
                button_list.append({'id': each.id,
                                    'title': each.title})
        return button_list

    def get_children(self, instance):
        # menus:用户所有的菜单
        role_menus = self.context['role_menus']
        role_buttons = self.context['role_buttons']
        # children列表
        children = []
        button_list = []
        temp = role_menus.filter(parent=instance).order_by('sort')

        for t in temp:
            item = MenuButtonTreeSerializer(t, context={'role_menus': role_menus,
                                                        'role_buttons': role_buttons})
            children.append(item.data)
        return children
