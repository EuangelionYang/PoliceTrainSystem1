# -*- coding: utf-8 -*-
# @Time : 2022/4/1 11:28
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : initialize.py
# @Software: PyCharm
import os
import uuid

import django
# 初始化程序代码，python manage.py init执行该段代码。。。。
# 初始化管理员账号、角色、菜单、部门。。。。。。
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
# django.setup()
# 角色模块，默认初始化4个角色
# 项目init 初始化，默认会执行 main 方法进行初始化
from django.contrib.auth.hashers import make_password
from utils.core_initialize import CoreInitialize
from rbac.models import *
class Initialize(CoreInitialize):
    # 初始化角色、岗位、部门、
    def init_post(self):
        self.post_data =[
            {"id":'9596bc9f-e2fd-4915-9077-1caa563aab45',"title":"管理","sort":1},]
        self.save(Post,self.post_data,"岗位信息")

    def init_dept(self):
        self.dept_data = [
            {"id":1,"title":"一级管理部门","leader_id":None,"sort":0,"telephone":None}
        ]
        self.save(Dept,self.dept_data,"部门信息")

    def init_role(self):
        self.role_data = [
            {"id":"2bef5b76-40ef-44a9-b5fa-1aeb5b61324f","title":"系统管理员","status":1,"identifier":"admin","menus":[1,2,3,4,5]},
            {"id":"91c169b1-f5f8-4037-9023-8a9920be4642","title":"学员","status":1,"identifier":"student","menus":[6,8,10,12,16]},
            {"id":"d678edc6-e7f8-497d-914b-145a34386c38","title":"教官","status":1,"identifier":"teacher","menus": [6,7,9,10,12,13,14,15,11,16]},
            {"id":"d951ce85-a1ec-4855-a48f-0470def0ca76","title":"教务管理","status":1,"identifier":"education","menus": [6,7,10,11,12,13,16]},]
        self.save(Role,self.role_data,"角色信息")

    def init_menu(self):
        self.menu_data = [
            {"id":1,"title":"系统管理","icon":"system","sort":2,"path":'/system',"parent_id":None,"component":"Layout","redirect":"/system/users",
             "hidden":False,"name":"system"},
            {"id":2,"title":"用户管理","icon":"user","sort":1,"path":'users',"parent_id":1,"component":"/system/user/index","redirect":None,
             "hidden":False,"name":"users"},
            {"id":3,"title":"角色管理","icon":"lock","sort":2,"path":'permission',"parent_id":1,"component":"/system/role/index","redirect":None,
             "hidden":False,"name":"permission"},
            {"id":4,"title":"部门管理","icon":"tree","sort":3,"path":'department',"parent_id":1,"component":"/system/dept/index","redirect":None,
             "hidden":False,"name":"department"},
            {"id":5,"title":"岗位管理","icon":"post","sort":4,"path":'post',"parent_id":1,"component":"/system/post/index","redirect":None,
             "hidden":False,"name":"post"},
            {"id":6,"title":"训练管理","icon":"example","sort":1,"path":'/training',"parent_id":None,"component":"Layout","redirect":"/training/study",
             "hidden":False,"name":"train"},
            {"id":7,"title":"训练列表","icon":"form","sort":1,"path":'lessonList',"parent_id":6,"component":"/lesson/lessonSys/lessonList","redirect":None,
             "hidden":False,"name":"trainList"},
            {"id":8,"title":"训练大厅","icon":"education","sort":2,"path":'study',"parent_id":6,"component":"/lesson/study/index","redirect":None,
             "hidden":False,"name":"study"},
            {"id":9,"title":"发布训练","icon":"edit","sort":3,"path":'upload',"parent_id":6,"component":"/lesson/lessonSys/upload","redirect":None,
             "hidden":True,"name":"upload"},
            {"id":10,"title":"训练详情","icon":None,"sort":5,"path":'studyDetail',"parent_id":6,"component":"/lesson/study/detail/studyDetail","redirect":None,
             "hidden":True,"name":"studyDetail"},
            {"id":11,"title":"审核训练","icon":"check","sort":6,"path":'check',"parent_id":6,"component":"/lesson/lessonSys/check","redirect":None,
             "hidden":True,"name":"check"},
            {"id":12,"title":"成绩管理","icon":"grade","sort":3,"path":'/score',"parent_id":None,"component":"Layout","redirect":'/score/statics',
             "hidden":False,"name":"score"},
            {"id":13,"title":"训练成绩统计","icon":"statics","sort":1,"path":'statics',"parent_id":12,"component":"/score/statics/index","redirect":None,
             "hidden":False,"name":"statics"},
            {"id":14,"title":"分类管理","icon":"cate","sort":4,"path":'cate',"parent_id":6,"component":"/lesson/categories/index","redirect":None,
             "hidden":False,"name":"cate"},
            {"id":15,"title":"动作管理","icon":"action","sort":7,"path":'action',"parent_id":6,"component":"/lesson/action","redirect":None,
             "hidden":False,"name":"action"},
            {"id":16,"title":"学员成绩分析","icon":"analysis","sort":2,"path":'analysis',"parent_id":12,"component":"/score/analysis/index","redirect":None,
             "hidden":False,"name":"analysis"},
        ]
        self.save(Menu,self.menu_data,"菜单信息")

        self.menu_button_data = [
            {"id":1,"title":'更新',"value":'update',"api":'/api/rbac/user/','method':2,"menu_id":2},
            {"id":2,"title":'查询',"value":'list',"api":'/api/rbac/user/','method':0,"menu_id":2},
            {"id":3,"title":'单例',"value":'retrieve',"api":'/api/rbac/user/{id}','method':0,"menu_id":2},
            {"id":4,"title":'删除',"value":'delete',"api":'/api/rbac/user/{id}','method':4,"menu_id":2},
            {"id":5,"title":'新增',"value":'create',"api":'/api/rbac/user/{id}','method':1,"menu_id":2},
            {"id":6, "title": '更新', "value": 'update', "api": '/api/rbac/role/', 'method': 2, "menu_id": 3},
            {"id":7,"title":'查询',"value":'list',"api":'/api/rbac/role/','method':0,"menu_id":3},
            {"id":8,"title":'单例',"value":'retrieve',"api":'/api/rbac/role/{id}','method':0,"menu_id":3},
            {"id":9,"title":'删除',"value":'delete',"api":'/api/rbac/role/{id}','method':4,"menu_id":3},
            {"id":10,"title":'新增',"value":'create',"api":'/api/rbac/role/{id}','method':1,"menu_id":3},
            {"id":11, "title": '更新', "value": 'update', "api": '/api/rbac/dept/', 'method': 2, "menu_id": 4},
            {"id":12,"title":'查询',"value":'list',"api":'/api/rbac/dept/','method':0,"menu_id":4},
            {"id":13,"title":'单例',"value":'retrieve',"api":'/api/rbac/dept/{id}','method':0,"menu_id":4},
            {"id":14,"title":'删除',"value":'delete',"api":'/api/rbac/dept/{id}','method':4,"menu_id":4},
            {"id":15,"title":'新增',"value":'create',"api":'/api/rbac/dept/{id}','method':1,"menu_id":4},
            {"id":16, "title": '更新', "value": 'update', "api": '/api/rbac/post/', 'method': 2, "menu_id": 5},
            {"id":17,"title":'查询',"value":'list',"api":'/api/rbac/post/','method':0,"menu_id":5},
            {"id":18,"title":'单例',"value":'retrieve',"api":'/api/rbac/post/{id}','method':0,"menu_id":5},
            {"id":19,"title":'删除',"value":'delete',"api":'/api/rbac/post/{id}','method':4,"menu_id":5},
            {"id":20,"title":'新增',"value":'create',"api":'/api/rbac/post/{id}','method':1,"menu_id":5},
        ]
        self.save(MenuButton, self.menu_button_data,"菜单-权限表")

    def init_user(self):
        user_data = [
            {'id':1,'username':'admin','password':'pbkdf2_sha256$260000$56Lk1GagZchvz73sbhewWc$404YaQMoN1ZlNgMVAeAzxh1U5BlXMOsrKLtzz2KSghc=',
             'is_active':True,'is_admin':True,'name':'admin',
             'role':['2bef5b76-40ef-44a9-b5fa-1aeb5b61324f'],},
             {'id':2,'username':'student','password':'pbkdf2_sha256$260000$z0D5gu5V06lbM2iFzB6cIY$u/6ArERCGvgBAxCb8rQ6X4/oPpxIRgyCuD76UZUwA1I=',
             'is_active':True,'is_admin':False,'name':'学员',
             'role':['91c169b1-f5f8-4037-9023-8a9920be4642'],},
              {'id':3,'username':'teacher','password':'pbkdf2_sha256$260000$Z6kvxodbcE4s42ATsjViMk$wo5/AaY6NgWZPlYKoqunnbuePdJI589GIbmimVKBjRQ=',
             'is_active':True,'is_admin':False,'name':'教官',
             'role':['d678edc6-e7f8-497d-914b-145a34386c38'],},
               {'id':4,'username':'manager','password':'pbkdf2_sha256$260000$Rz5THC2VkLzfFMLqPwXgpr$FdBrUQ4WU2wEFYafQ4RrLG06wTSBFpplIoxUmdIkqDo=',
             'is_active':True,'is_admin':False,'name':'教务管理',
             'role':['d951ce85-a1ec-4855-a48f-0470def0ca76'],
    },
        ]
        self.save(User,user_data,"用户信息")

    def run(self):
        self.init_post()
        self.init_dept()
        self.init_menu()
        self.init_role()
        self.init_user()

def main(reset=False):
    Initialize(reset).run()
    pass

if __name__ == '__main__':
    main()