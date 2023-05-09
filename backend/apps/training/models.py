import datetime
import uuid

from django.db import models
from django.db.models.signals import pre_delete, post_init, post_save
from django.dispatch.dispatcher import receiver
# Create your models here.
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


class Category(models.Model):
    title = models.CharField(unique=True, max_length=255, verbose_name='分类名称', null=True, blank=True)
    sort = models.IntegerField(default=0, blank=True, null=True, verbose_name='分类排序')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='分类创建时间')
    type = models.CharField(max_length=10, verbose_name='分类类型', blank=True, null=True, default=0)

    class Meta:
        ordering = ['sort']


class Training(models.Model):
    """
    训练实体
    TrainingID：课程编号，唯一
    TrainingName：课程名称
    detail：课程的描述信息，可为空
    learners：学员，多对多关系,learner.lessons可以查询学员选修的所有课程
    classify:
    """

    def file_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'training/cover/{}/{}'.format(datetime.date.today(), uuid.uuid4())

    TrainingID = models.CharField(unique=True, max_length=255, verbose_name='训练编号')
    TrainingName = models.CharField(max_length=255, verbose_name='训练名称')
    cover = models.ImageField(verbose_name='训练封面', upload_to=file_path, null=True, blank=True)
    cover_clip = ImageSpecField(
        source="cover",
        processors=[ResizeToFill(400, 250)],
        format='JPEG',
        options={'quality': 95}
    )
    teacher = models.ForeignKey(to='rbac.User', related_name='teach', blank=True, null=True, on_delete=models.SET_NULL)
    detail = models.CharField(verbose_name='描述信息', max_length=255, blank=True, null=True)
    learners = models.ManyToManyField('rbac.User', related_name='trainings',
                                      through='TrainingToLearner',
                                      through_fields=('training', 'learner')
                                      )
    is_publish = models.BooleanField(verbose_name='是否发布', default=False, blank=True, null=True)
    is_review = models.BooleanField(verbose_name='是否审核', default=False, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name='训练创建时间', auto_now_add=True)
    category = models.ForeignKey(to='Category', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='训练类别')

    class Meta:
        verbose_name = '训练'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return f"{self.TrainingName}"


# 删除时将训练封面一同删除
@receiver(pre_delete, sender=Training)
def cover_delete(sender, instance, **kwargs):
    print('删除训练的同时删除训练封面')
    instance.cover.delete(False)


@receiver(post_init, sender=Training)
def file_path(sender, instance, **kwargs):
    instance._current_file = instance.cover


@receiver(post_save, sender=Training)
def delete_old_cover(sender, instance, **kwargs):
    if hasattr(instance, '_current_file'):
        if instance._current_file != instance.cover:
            instance._current_file.delete(save=False)


class TrainingToLearner(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    learner = models.ForeignKey('rbac.User', on_delete=models.CASCADE)
    is_finish = models.BooleanField(verbose_name="训练状态", default=False, null=True, blank=True)
    grade = models.IntegerField(verbose_name='训练成绩', default=0, null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = "训练-学员"
        unique_together = ("learner", "training")


class Chapter(models.Model):
    """
    章节实体，要求用户需要按照一定的学习顺序学习
    chapterID：章节编号，唯一
    chapterTitle：章节名称
    chapterURL：章节的存放地址
    lessons：章节所属的课程，多对多关系，lesson.chapters可以查询课程下的所有章节
    learners：选修章节的学员，多对多关系，learner.chapters可以查询该学员选修的所有章节
    """

    chapterID = models.CharField(unique=True, max_length=255, verbose_name='章节编号')
    chapterTitle = models.CharField(max_length=255, verbose_name='章节名称', null=True, blank=True)
    type = models.CharField(max_length=255, verbose_name="课程类型", blank=True, null=True)
    sex = models.CharField(max_length=10, verbose_name="性别", blank=True, null=True, help_text='情绪课程性别')
    crime_type = models.CharField(max_length=10, verbose_name="犯罪类型", blank=True, null=True, help_text='情绪课程犯罪类型')
    age = models.CharField(max_length=10, verbose_name="罪犯年纪", blank=True, null=True, help_text='情绪课程罪犯年纪')
    mental = models.CharField(max_length=10, blank=True, null=True, help_text='情绪课程精神状态')
    crime_tendency = models.CharField(max_length=10, blank=True, null=True, help_text='情绪课程犯罪倾向')
    emotion = models.CharField(max_length=10, blank=True, null=True, help_text='情绪课程犯罪情绪')
    details = models.CharField(max_length=255, verbose_name='课程描述', blank=True, null=True, help_text='课程描述')

    def file_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'training/chapter/{}/{}'.format(datetime.date.today(), filename)

    # 'training/chapter/%Y%m%d/{}'
    chapterFile = models.FileField(upload_to=file_path, verbose_name='章节视频',
                                   null=True,
                                   blank=True)
    training = models.ForeignKey('training.Training',
                                 related_name='chapters',
                                 verbose_name='所属课程',
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    prevChapter = models.ForeignKey('training.Chapter', on_delete=models.SET_NULL,
                                    verbose_name='上一章节',
                                    null=True,
                                    blank=True)
    learners = models.ManyToManyField('rbac.User', related_name='chapters',
                                      through='training.ChapterToLearner',
                                      through_fields=('chapter', 'learner'))
    up_load_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        ordering = ['id']
        verbose_name = '训练章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.chapterTitle}"


# 删除时将课程文件一同删除
@receiver(pre_delete, sender=Chapter)
def chapter_delete(sender, instance, **kwargs):
    print('删除课程的同时删除课程文件')
    instance.chapterFile.delete(False)


@receiver(post_init, sender=Chapter)
def file_path(sender, instance, **kwargs):
    instance._current_file = instance.chapterFile


@receiver(post_save, sender=Chapter)
def delete_old_chapter(sender, instance, **kwargs):
    if hasattr(instance, '_current_file'):
        if instance._current_file != instance.chapterFile:
            instance._current_file.delete(save=False)


class ChapterToLearner(models.Model):
    chapter = models.ForeignKey('training.Chapter', on_delete=models.CASCADE)
    learner = models.ForeignKey('rbac.User', on_delete=models.CASCADE)
    is_finish = models.BooleanField(default=False, null=True, blank=True, verbose_name="学习状态")
    grade = models.IntegerField(default=0, null=True, blank=True, verbose_name='章节成绩')

    class Meta:
        ordering = ['id']


class TrainingPoint(models.Model):
    """
    moment:时刻
    action:标准动作
    duration:动作持续时间
    chapter:章节外键
    """
    # moment = models.FloatField(verbose_name="起始时刻", null=True, blank=True)
    action = models.ForeignKey(to='Action', verbose_name="标准动作", blank=True, null=True, related_name='action',
                               on_delete=models.SET_NULL)
    emotion = models.ForeignKey(to='Action', verbose_name="情绪", blank=True, null=True, related_name='emotion',
                                on_delete=models.SET_NULL)
    mood = models.ForeignKey(to='Action', verbose_name="语气", blank=True, null=True, related_name='mood',
                             on_delete=models.SET_NULL)
    # duration = models.IntegerField(verbose_name="持续时间", null=True, blank=True)
    chapter = models.ForeignKey(to='Chapter', on_delete=models.CASCADE, verbose_name='所属章节', related_name='points')
    start_time = models.IntegerField(verbose_name="开始时间", null=True, blank=True)
    end_time = models.IntegerField(verbose_name="结束时间", null=True, blank=True)

    # type = models.CharField()
    class Meta:
        ordering = ['id']


class Action(models.Model):
    actionName = models.CharField(verbose_name='动作名称', null=True, blank=True, max_length=255)
    identifier = models.CharField(verbose_name='动作标识符', unique=True, max_length=255)
    type = models.CharField(verbose_name='动作分类', null=True, blank=True, max_length=10)

    class Meta:
        ordering = ['id']


class ChapterGradeRecord(models.Model):
    chapter = models.ForeignKey(to='Chapter', on_delete=models.CASCADE, verbose_name='所属章节', related_name='records')
    learner = models.ForeignKey(to='rbac.User', on_delete=models.CASCADE, verbose_name='所属学员', related_name='records')
    grade = models.IntegerField(default=0, verbose_name='章节成绩')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='成绩上传时间')


class KeyFrame(models.Model):
    # 通过keyframe反向查询章节的所有keyframe
    chapter = models.ForeignKey(to='Chapter', on_delete=models.CASCADE, verbose_name='所属视频', related_name='keyframes')
    keyframe_time = models.IntegerField(default=0, verbose_name='关键帧时刻', blank=True, null=True)
    keyframe_Focus = models.IntegerField(default=0, verbose_name='关节点')
    keyframe_Skeleton = models.BinaryField(blank=True, null=True)
    keyframe_Description = models.CharField(max_length=255, blank=True, null=True, verbose_name='关键帧说明')
