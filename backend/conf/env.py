# -*- coding: utf-8 -*-
# @Time : 2022/5/30 16:02
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : env.py.py
# @Software: PyCharm

# ================================================= #
# ************** mysql数据库 配置  ************** #
# ================================================= #
# 数据库地址
dev = True
if dev:
    DATABASE_ENGINE = "django.db.backends.mysql"
    # 数据库地址
    DATABASE_HOST = "127.0.0.1"
    # 数据库端口
    DATABASE_PORT = 3306
    # 数据库用户名
    DATABASE_USER = "root"
    # 数据库密码
    DATABASE_PASSWORD = "19990318"
    # 数据库名
    DATABASE_NAME = "test"
else:
    DATABASE_ENGINE = "django.db.backends.mysql"
    # 数据库地址
    DATABASE_HOST = "121.195.154.165"
    # 数据库端口
    DATABASE_PORT = 3306
    # 数据库用户名
    DATABASE_USER = "root"
    # 数据库密码
    DATABASE_PASSWORD = "UrbanNet123!"
    # 数据库名
    DATABASE_NAME = "Police_Sys"
