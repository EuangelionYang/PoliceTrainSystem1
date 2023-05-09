# -*- coding: utf-8 -*-
# @Time : 2021/12/21 16:08
# @Author : YangYu
# @Email: yangyu.cs@outlook.com
# @File : urls.py
# @Software: PyCharm
from django.urls import re_path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

router.register('training', TrainingViewSet)
router.register('training_learner', TrainingToLearnerViewSet)
router.register('category', CategoryViewSet)
router.register('chapter', ChapterViewSet)
router.register('chapter_learner', ChapterToLearnerViewSet)
router.register('training_point', TrainingPointViewSet)
router.register('action', ActionViewSet)
router.register('keyframe', KeyFrameViewSet)
urlpatterns = [
    re_path('training/set_learners/', TrainingViewSet.as_view({'post': 'set_learners'})),
    re_path('training/publish/', TrainingViewSet.as_view({'post': 'publish'})),
    re_path('training/review/', TrainingViewSet.as_view({'post': 'review'})),
    re_path('training/get_chaptersByTrainingID/', TrainingViewSet.as_view({'post': 'get_chaptersByTrainingID'})),
    re_path('chapter/get_pointsByChapterID/', ChapterViewSet.as_view({'post': 'get_pointsByChapterID'})),
    re_path('chapter/get_keyframeByChapterID/', ChapterViewSet.as_view({'post': 'get_keyframeByChapterID'})),
    re_path('training/get_trainingByUser/', TrainingViewSet.as_view({'post': 'get_trainingByUser'})),
    re_path('training/get_trainingByTeacher/', TrainingViewSet.as_view({'get': 'get_trainingByTeacher'})),
    re_path('training/get_chapter_grade/', TrainingViewSet.as_view({'post': 'get_chapter_grade'})),
    re_path('training/submit_chapter_grade/', TrainingViewSet.as_view({'post': 'submit_chapter_grade'})),
    re_path('training/get_chapter_history_grade/', TrainingViewSet.as_view({'post': 'get_chapter_history_grade'})),
    re_path('training/get_teachers/', TrainingViewSet.as_view({'get': 'get_teachers'})),
    re_path('training/get_learners/', TrainingViewSet.as_view({'get': 'get_learners'})),
    re_path('training/get_learners_grade/', TrainingViewSet.as_view({'get': 'get_learners_grade'})),
    re_path('training/my_grade/', TrainingViewSet.as_view({'get': 'get_myGrade'})),
    re_path('upload/', Upload.as_view()),
    re_path('keyframe/create_keyframe/', KeyFrameViewSet.as_view({'post': 'create_keyframe'})),
    re_path('complete/', Complete.as_view()),
    # re_path('keyframe/', KeyFrame.as_view()),
]
urlpatterns += router.urls
