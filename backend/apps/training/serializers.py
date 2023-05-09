# -*- coding: utf-8 -*-
# @Time : 2021/12/21 16:05
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : serializers.py
# @Software: PyCharm
import os
import shutil
import traceback

from django.core.files.base import ContentFile, File
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from .models import *
from utils.serializers import customModelSerializer

from rbac.models import User

from PoliceTrainSystem.settings import MEDIA_ROOT


class CategorySerializer(customModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LearnerSerializer(customModelSerializer):
    dept_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'dept_name']

    def get_dept_name(self, instance):
        dept = instance.dept
        dept_name = None
        dept_stack = []
        while dept:
            dept_name = ''
            dept_stack.append(dept.title)
            dept = dept.parent
        while len(dept_stack) > 0:
            dept_name += dept_stack.pop()
            if len(dept_stack) > 0:
                dept_name += '-'
        return dept_name


class TrainingSerializer(customModelSerializer):
    learner_list = serializers.SerializerMethodField(read_only=True)
    learner_number = serializers.SerializerMethodField(read_only=True)
    teacher_name = serializers.StringRelatedField(source='teacher.name', read_only=True)

    class Meta:
        model = Training
        fields = '__all__'

    def get_learner_list(self, instance):
        learner_list = []
        learners = instance.learners.all()
        for each in learners:
            learner_list.append({'learner_id': each.id,
                                 'learner_name': each.name})
        return learner_list

    def get_learner_number(self, instance):
        number = instance.learners.all().count()
        return number


class TrainingToLearnerSerializer(customModelSerializer):
    class Meta:
        model = TrainingToLearner
        fields = '__all__'


class ChapterSerializer(customModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'


class ChapterCreateSerializer(customModelSerializer):
    class Meta:
        model = Chapter
        exclude = ['chapterFile']

    def create(self, validated_data):
        url = self.request.POST.get('url', None)
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # os.chdir(MEDIA_ROOT)
        dst_dir = f'training/chapter/{current_date}/'
        # if not os.path.exists(dst_dir):
        #     os.makedirs(dst_dir)
        # # new_url = os.path.join(dst_dir,os.path.split(url)[1])
        # new_url = os.path.split(url)[1]
        # # print(new_url)
        # if os.path.isfile(url):
        #     shutil.move(url, new_url)
        #     file = File(open(new_url, 'rb'))
        # else:
        #     raise FileNotFoundError('上传文件失败，请重新上传文件！')
        file = File(open(url, 'rb'))
        instance = super().create(validated_data)
        filename = os.path.split(file.name)[1]
        instance.chapterFile.save(filename, file, save=True)
        instance.save()
        file.close()
        os.remove(url)
        return instance

    def update(self, instance, validated_data):
        url = self.request.POST.get('url', None)
        instance = super().update(instance, validated_data)
        if url:
            with open(url, 'rb') as file:
                filename = os.path.split(file.name)[1]
                instance.chapterFile.save(filename, file, save=True)
                instance.save()
            os.remove(url)
        return instance


class ChapterToLearnerSerializer(customModelSerializer):
    class Meta:
        model = ChapterToLearner
        fields = '__all__'


class TrainingPointSerializer(customModelSerializer):
    action_name = serializers.StringRelatedField(source='action.actionName', read_only=True)
    emotion_name = serializers.StringRelatedField(source='emotion.actionName', read_only=True)
    mood_name = serializers.StringRelatedField(source='mood.actionName', read_only=True)

    class Meta:
        model = TrainingPoint
        fields = '__all__'


class ActionSerializer(customModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class TrainingGradeSerializer(customModelSerializer):
    learners = serializers.SerializerMethodField()
    teacher = serializers.StringRelatedField(source='teacher.name', read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    def get_learners(self, instance):
        # 通过训练，查询该训练下的所有学员，将训练-学员表中的记录按成绩排序
        tls = TrainingToLearner.objects.filter(training=instance).order_by('grade')
        res = []
        finish = 0
        total = 0
        for each in tls:
            res.append(
                {'id': each.learner.id,
                 'name': each.learner.name,
                 'grade': each.grade,
                 'is_finish': each.is_finish})
            if each.is_finish == True:
                finish = finish + 1
            total = total + 1
        return {'total': total, 'finish': finish,
                'detail': res
                }

    class Meta:
        model = Training
        fields = ['id', 'TrainingID', 'TrainingName', 'teacher', 'category', 'learners']


class LearnerGradeRecord(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.StringRelatedField(read_only=True)
    trainings = serializers.SerializerMethodField()

    def get_trainings(self, instance):
        trainings = TrainingToLearner.objects.filter(learner=instance).order_by('grade')
        res = []
        for each in trainings:
            res.append({'training': each.training.TrainingName,
                        'finish': each.is_finish,
                        'grade': each.grade})
        return res


class KeyFrameSerializer(customModelSerializer):
    class Meta:
        model = KeyFrame
        # fields = '__all__'
        exclude = ['keyframe_Skeleton']


class KeyFrameUpdateSerializer(customModelSerializer):
    class Meta:
        model = KeyFrame
        # fields = '__all__'
        # fields = ['id', 'keyframe_Focus']
        exclude = ['keyframe_Skeleton']
