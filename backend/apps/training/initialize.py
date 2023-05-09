# -*- coding: utf-8 -*-
# @Time : 2023/4/13 20:59
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : initialize.py
# @Software: PyCharm
from utils.core_initialize import CoreInitialize
from apps.training.models import *


class Initialize(CoreInitialize):
    def init_category(self):
        self.category_data = [
            {"id": 1, 'title': '动作识别', 'sort': 1, 'type': "课程分类"},
            {"id": 2, 'title': '情绪识别', 'sort': 1, 'type': "课程分类"},
            {"id": 3, 'title': '心理识别', 'sort': 1, 'type': "课程分类"},
            {"id": 4, 'title': '动作规范', 'sort': 1, 'type': "课程分类"},
        ]
        self.save(Category, self.category_data, "分类数据")

    def init_action(self):
        self.action_data = [
            {"id": 1, 'actionName': '直拳', 'identifier': 'zhiquan', 'type': '动作'},
            {"id": 2, 'actionName': '肘击', 'identifier': 'zhouji', 'type': '动作'},
            {"id": 3, 'actionName': '勾拳', 'identifier': 'gouquan', 'type': '动作'},
            {"id": 4, 'actionName': '戒备', 'identifier': 'jiebei', 'type': '动作'},
            {"id": 5, 'actionName': '格挡', 'identifier': 'gedang', 'type': '动作'},
            {"id": 6, 'actionName': '闪躲', 'identifier': 'shanduo', 'type': '动作'},
            {"id": 7, 'actionName': '踢腿', 'identifier': 'titui', 'type': '动作'},
            {"id": 8, 'actionName': '提膝', 'identifier': 'tixi', 'type': '动作'},
            {"id": 9, 'actionName': '左肩', 'identifier': 'zuojian', 'type': '关节'},
            {"id": 10, 'actionName': '右肩', 'identifier': 'youjian', 'type': '关节'},
            {"id": 11, 'actionName': '左肘', 'identifier': 'zuozhou', 'type': '关节'},
            {"id": 12, 'actionName': '右肘', 'identifier': 'youzhou', 'type': '关节'},
            {"id": 13, 'actionName': '左腕', 'identifier': 'zuowan', 'type': '关节'},
            {"id": 14, 'actionName': '右腕', 'identifier': 'youwan', 'type': '关节'},
            {"id": 15, 'actionName': '左脚', 'identifier': 'zuojiao', 'type': '关节'},
            {"id": 16, 'actionName': '右脚', 'identifier': 'youjiao', 'type': '关节'},
            {"id": 17, 'actionName': '左膝', 'identifier': 'zuoxi', 'type': '关节'},
            {"id": 18, 'actionName': '右膝', 'identifier': 'youxi', 'type': '关节'},
            {"id": 19, 'actionName': '高兴', 'identifier': 'gaoxing', 'type': '情绪'},
            {"id": 20, 'actionName': '生气', 'identifier': 'shengqi', 'type': '情绪'},
            {"id": 21, 'actionName': '厌恶', 'identifier': 'yanwu', 'type': '情绪'},
            {"id": 22, 'actionName': '害怕', 'identifier': 'haipa', 'type': '情绪'},
            {"id": 23, 'actionName': '伤心', 'identifier': 'shangxin', 'type': '情绪'},
            {"id": 24, 'actionName': '积极', 'identifier': 'jiji', 'type': '心理'},
            {"id": 25, 'actionName': '消极', 'identifier': 'xiaoji', 'type': '心理'},
            {"id": 26, 'actionName': '平静', 'identifier': 'pingjing', 'type': '心理'},
            {"id": 27, 'actionName': '反问语气', 'identifier': 'fanwen', 'type': '语气'},
            {"id": 28, 'actionName': '疑问语气', 'identifier': 'yiwen', 'type': '语气'},
            {"id": 29, 'actionName': '陈述语气', 'identifier': 'chenshu', 'type': '语气'},
            {"id": 30, 'actionName': '命令语气', 'identifier': 'mingling', 'type': '语气'},
            {"id": 31, 'actionName': '请求语气', 'identifier': 'qingqiu', 'type': '语气'},
        ]
        self.save(Action, self.action_data, "动作信息")

    def run(self):
        self.init_action()
        self.init_category()


def main(reset=False):
    Initialize(reset).run()
    pass


if __name__ == '__main__':
    main()
