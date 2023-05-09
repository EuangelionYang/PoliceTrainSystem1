import os
from datetime import time

from django.shortcuts import render
from PoliceTrainSystem.settings import MEDIA_ROOT, BASE_DIR

# Create your views here.
from rest_framework.views import APIView
from utils.viewset import customModelViewSet

from .demo_sken import create_keyframe
from .models import *
from .serializers import *
from utils.response import APIResponse

from rbac.serializers import userSerializer

from rbac.models import Role


class CategoryViewSet(customModelViewSet):
    permission_classes = []
    queryset = Category.objects.all()
    filter_fields = ('type',)
    serializer_class = CategorySerializer


class TrainingViewSet(customModelViewSet):
    permission_classes = []
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    search_fields = ('TrainingName', 'teacher__name', 'TrainingID')
    filter_fileds = ('is_publish', 'is_review',)

    def get_chaptersByTrainingID(self, request):
        tid = request.data['training_id']
        training = Training.objects.get(id=tid)
        chapters = training.chapters.all()
        serializer = ChapterSerializer(instance=chapters, many=True, context={'request': request})
        return APIResponse(data=serializer.data, msg='获取章节成功')

    def set_learners(self, request):
        """
        设置学员,添加新增的学员，删除不在learner_ids里面的学员
        """
        training_id = request.data['training_id']
        learner_ids = request.data['learner_ids']
        # training = Training(id=training_id)
        chapter_list = Training.objects.get(id=training_id).chapters.all()
        # print(chapter_list)
        tls = []
        cls = []
        # 添加操作
        for each in learner_ids:
            if TrainingToLearner.objects.filter(training_id=training_id, learner_id=each).exists():
                continue
            tl = TrainingToLearner(training_id=training_id, learner_id=each,
                                   is_finish=False, grade=0)
            tls.append(tl)
            for chap in chapter_list:
                if ChapterToLearner.objects.filter(chapter_id=chap.id, learner_id=each).exists():
                    continue
                cl = ChapterToLearner(chapter_id=chap.id, learner_id=each, is_finish=False, grade=0)
                cls.append(cl)

            # if ChapterToLearner
        TrainingToLearner.objects.bulk_create(tls)
        ChapterToLearner.objects.bulk_create(cls)
        # 删除操作
        # 删除学员的训练
        training_learner_obj = TrainingToLearner.objects.filter(training_id=training_id)
        training_delete_obj = training_learner_obj.exclude(learner_id__in=learner_ids)
        training_delete_obj.delete()
        # 删除学员的章节
        for chap in chapter_list:
            chapter_learner_obj = ChapterToLearner.objects.filter(chapter_id=chap.id)
            chapter_delete_obj = chapter_learner_obj.exclude(learner_id__in=learner_ids)
            chapter_delete_obj.delete()
        return APIResponse(msg='设置学员成功')

    def publish(self, request):
        """
        发布时，只能发布教务分配给教官的训练
        """
        user = request.user
        training_id = request.data['training_id']
        training = Training.objects.get(id=training_id)
        # print(user is not training.teacher)
        if user != training.teacher:
            raise PermissionError('您无权发布此训练！')
        training.is_publish = True
        training.save()
        return APIResponse(msg='发布课程成功')

    def review(self, request):
        is_pass = int(request.data['is_pass'])
        user = request.user
        training_id = request.data['training_id']
        training = Training.objects.get(id=training_id)
        if is_pass == 1 and training.is_publish == True:
            training.is_review = True
            training.save()
            return APIResponse(msg='审核通过！')
        # 审核通过
        elif is_pass == 0:
            # 审核驳回
            training.is_publish = False
            training.is_review = False
            training.save()
            return APIResponse(msg='驳回课程！')
        else:
            raise ValueError('请求参数错误！')

    def get_trainingByUser(self, request):
        uid = request.data['uid']
        user = User.objects.get(id=uid)
        category = request.query_params.get('category', None)
        training = user.trainings.filter(is_review=True, is_publish=True)
        # print(category)
        if category:
            training = training.filter(category=category)
        # print(2)
        for backend in set(set(self.filter_backends) | set(self.extra_filter_backends or [])):
            training = backend().filter_queryset(self.request, training, self)
        no_page = request.query_params.get('no_page', None)
        if no_page is None:
            page = self.paginate_queryset(training)
        else:
            page = None
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TrainingSerializer(instance=training, many=True, context={'request': request})
        return APIResponse(data=serializer.data, msg='获取训练成功')

    def get_trainingByTeacher(self, request):
        tid = request.query_params.get('teacher_id', None)
        if tid is None:
            raise ValueError('参数非法！')
        teacher = User.objects.get(id=tid)
        # print(teacher)
        training = teacher.teach.all()
        # print(training)
        for backend in set(set(self.filter_backends) | set(self.extra_filter_backends or [])):
            training = backend().filter_queryset(self.request, training, self)
        no_page = request.query_params.get('no_page', None)
        if no_page is None:
            page = self.paginate_queryset(training)
        else:
            page = None
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TrainingSerializer(instance=training, many=True, context={'request': request})
        return APIResponse(data=serializer.data, msg='获取训练成功')

    def get_chapter_grade(self, request):
        training_id = request.data['training_id']
        training = Training.objects.get(id=training_id)
        learner_id = request.data['learner_id']
        learner = User.objects.get(id=learner_id)
        tl = TrainingToLearner.objects.get(training=training, learner=learner)
        chapter = Chapter.objects.filter(training=training)

        data = {'trainingName': training.TrainingName,
                'is_finish': tl.is_finish,
                'chapters': []}
        for each in chapter:
            cl = ChapterToLearner.objects.get(learner=learner_id, chapter=each)
            data['chapters'].append({
                'chapterID': each.id,
                'chapterName': each.chapterTitle,
                'grade': cl.grade,
                'is_finish': cl.is_finish
            })
        return APIResponse(msg='获取成绩成功', data=data)

    def submit_chapter_grade(self, request):
        cid = request.data['chapter_id']
        chapter = Chapter.objects.get(id=cid)
        lid = request.data['learner_id']
        learner = User.objects.get(id=lid)
        grade = int(request.data['grade'])
        cgr = ChapterGradeRecord(chapter=chapter, learner=learner, grade=grade)
        cgr.save()
        ctl = ChapterToLearner.objects.get(chapter=chapter, learner=learner)
        if ctl.grade < grade:
            ctl.grade = grade

        ctl.is_finish = True
        ctl.save()
        training = chapter.training
        chapters = training.chapters.all()
        tl = TrainingToLearner.objects.get(training=training, learner=learner)
        tl.is_finish = True
        tl.grade = 0
        for each in chapters:
            temp = ChapterToLearner.objects.get(chapter=each, learner=learner)
            if temp.is_finish == False:
                tl.is_finish = False
            tl.grade = tl.grade + temp.grade
            # print(tl.grade)
        tl.grade = tl.grade / len(chapters)
        tl.save()
        return APIResponse(msg='提交成功')

    def get_chapter_history_grade(self, request):
        training_id = request.data['training_id']
        training = Training.objects.get(id=training_id)
        learner_id = request.data['learner_id']
        learner = User.objects.get(id=learner_id)
        tl = TrainingToLearner.objects.get(training=training, learner=learner)
        chapters = training.chapters.all()
        data = {'trainingName': training.TrainingName,
                'is_finish': tl.is_finish,
                'chapters': []
                }
        for each in chapters:
            cgr = ChapterGradeRecord.objects.filter(learner=learner, chapter=each).order_by('upload_time')
            dic = {'chapterName': each.chapterTitle,
                   'grades': [],
                   'submit_time': []
                   }
            for t in cgr:
                dic['grades'].append(t.grade)
                # print(type(t.upload_time))
                dic['submit_time'].append(t.upload_time.strftime('%Y-%m-%d %H:%M:%S'))
            data['chapters'].append(dic)

        return APIResponse(data=data)

    def get_teachers(self, request):
        teachers = Role.objects.get(identifier="teacher").user_set.all()
        serializer = userSerializer(instance=teachers, many=True)
        return APIResponse(msg='获取教官成功', data=serializer.data)

    def get_learners(self, request):
        learners = Role.objects.get(identifier="student").user_set.all()
        serializer = userSerializer(instance=learners, many=True)
        return APIResponse(msg='获取学员成功', data=serializer.data)

    def get_learners_grade(self, request):
        training_id = request.query_params['training_id']
        training = Training.objects.get(id=training_id)
        serializer = TrainingGradeSerializer(instance=training)
        return APIResponse(msg='获取成绩成功', data=serializer.data)

    def get_myGrade(self, request):
        user_id = request.query_params.get('user_id', None)
        if user_id is None:
            raise ValueError('请传入参数')
        user = User.objects.get(id=request.query_params['user_id'])
        serializer = LearnerGradeRecord(instance=user)
        return APIResponse(msg='获取成绩单成功', data=serializer.data)


class TrainingToLearnerViewSet(customModelViewSet):
    permission_classes = []
    queryset = TrainingToLearner.objects.all()
    serializer_class = TrainingToLearnerSerializer


class ChapterViewSet(customModelViewSet):
    permission_classes = []
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    create_serializer_class = ChapterCreateSerializer
    update_serializer_class = ChapterCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        id = serializer.data['id']
        chapter = Chapter.objects.get(id=id)
        training = chapter.training
        learners = training.learners.all()
        chapter.learners.set(learners)
        chapter.save()
        serializer = self.get_serializer(instance=chapter)
        return APIResponse(data=serializer.data, msg="新增成功")

    def get_pointsByChapterID(self, request):
        chapter_id = request.data['chapter_id']
        chapter = Chapter.objects.get(id=chapter_id)
        points = chapter.points.all()
        serializer = TrainingPointSerializer(instance=points, many=True)
        return APIResponse(data=serializer.data, msg='获取训练点成功')

    def get_keyframeByChapterID(self, request):
        chapter_id = request.data['chapter_id']
        chapter = Chapter.objects.get(id=chapter_id)
        keyframes = chapter.keyframes.all()
        serializer = KeyFrameSerializer(instance=keyframes, many=True)
        return APIResponse(data=serializer.data, msg='获取关键帧成功')


class ChapterToLearnerViewSet(customModelViewSet):
    permission_classes = []
    queryset = ChapterToLearner.objects.all()
    serializer_class = ChapterToLearnerSerializer


class TrainingPointViewSet(customModelViewSet):
    permission_classes = []
    queryset = TrainingPoint.objects.all()
    serializer_class = TrainingPointSerializer


class ActionViewSet(customModelViewSet):
    permission_classes = []
    queryset = Action.objects.all()
    filter_fields = ('type',)
    serializer_class = ActionSerializer


class Upload(APIView):
    def post(self, request):
        chunk = request.data['chunkNumber']
        file = request.data['file']
        identifier = request.data['identifier']
        tmp_path = 'media/upload/temp/' + identifier
        tmp_path = os.path.join(MEDIA_ROOT, 'upload/temp/', identifier)

        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        with open(os.path.join(tmp_path, chunk), 'wb') as chunk:
            for buf in file.chunks():
                chunk.write(buf)
        return APIResponse(msg='ok', data={'code': 0})


class Complete(APIView):
    def post(self, request):
        chunk = 0
        identifier = request.data['identifier']
        file_name = request.data['file_name']
        tmp_path = os.path.join(MEDIA_ROOT, 'upload/temp/', identifier)
        # print(tmp_path)
        dst = os.path.join(MEDIA_ROOT, 'upload/temp/', file_name)
        with open(dst, 'wb') as file_complete:
            while True:
                try:
                    chunk_path = os.path.join(tmp_path, str(chunk))
                    # print(chunk_path)
                    file_clip = open(chunk_path, 'rb')
                    file_complete.write(file_clip.read())
                    file_clip.close()
                except IOError:
                    break
                chunk += 1
                os.remove(chunk_path)
        os.rmdir(tmp_path)
        return APIResponse(code=200, data={'url': file_complete.name})


class KeyFrameViewSet(customModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = KeyFrame.objects.all()
    serializer_class = KeyFrameSerializer
    update_serializer_class = KeyFrameUpdateSerializer

    def create_keyframe(self, request):
        chapter_id = request.data['chapter_id']
        chapter_obj = Chapter.objects.get(id=chapter_id)
        file_path = os.path.join(MEDIA_ROOT, str(chapter_obj.chapterFile))
        create_keyframe(chapter_id, file_path)
        return APIResponse(msg='ok')


class KeyFrame(APIView):
    # 创建关键帧
    """
    1. 通过post方式传入视频id
    2. 查找视频的路径，对该视频调用create_keyframe生成关键帧
    3. 保存关键帧到数据库
    4. 将关键帧回显到前端
    """

    def post(self, request):
        chapter_id = request.data['chapter_id']
        chapter_obj = Chapter.objects.get(id=chapter_id)
        # print(chapter_obj.chapterFile)
        file_path = os.path.join(MEDIA_ROOT, str(chapter_obj.chapterFile))
        # print(file_path)
        create_keyframe(chapter_id, file_path)

        return APIResponse(msg='ok')
