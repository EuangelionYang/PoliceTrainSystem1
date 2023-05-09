# -*- coding: utf-8 -*-
# @Time : 2022/4/1 11:15
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : init.py
# @Software: PyCharm
from django.core.management.base import BaseCommand

from PoliceTrainSystem import settings


class Command(BaseCommand):
    """
    项目初始化命令: python manage.py init
    """
    # 添加参数
    def add_arguments(self, parser):
        parser.add_argument('init_name', nargs='*', type=str, )
        parser.add_argument('-y', nargs='*')
        parser.add_argument('-Y', nargs='*')
        parser.add_argument('-n', nargs='*')
        parser.add_argument('-N', nargs='*')

    def handle(self, *args, **options):
        # 是否要重置
        reset = False
        if isinstance(options.get('y'), list) or isinstance(options.get('Y'), list):
            print('chongzhi')
            reset = True
        if isinstance(options.get('n'), list) or isinstance(options.get('N'), list):
            reset = False
            print('buchongzhi')
        print(f"正在准备初始化数据，{'如有初始化数据，将会不做操作跳过' if not reset else '初始数据将会先删除后新增'}...")

        for app in settings.INSTALLED_APPS:
            try:
                exec(f"""
from {app}.initialize import main
main(reset={reset})
                """)
            except ModuleNotFoundError:
                pass
        print("初始化数据完成！")
