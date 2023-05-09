import uuid

from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import pre_delete, post_init, post_save
from django.dispatch.dispatcher import receiver


class Menu(models.Model):
    """
    后端需要返回的response格式
    [
    {
        "path": "/permission",
        "component": "Layout",
        "meta": {
            "title": "权限管理",8
            "icon": "el-icon-lock"
        },
        "name": "permission",
        "redirect": "/permission/users",
        "alwaysShow": true,
        "children": [
            {
                "path": "users",
                "name": "users",
                "component": "permission/user",
                "meta": {
                    "title": "用户列表",
                    "icon": "el-icon-user"
                },
                "hidden": false
            }
        ]
    }]

    """
    # 菜单是个树形结构。
    parent = models.ForeignKey(to='rbac.Menu', verbose_name='父级菜单',
                               db_constraint=False, on_delete=models.CASCADE, null=True, blank=True)
    # meta.title & meta.icon
    title = models.CharField(verbose_name='菜单名称', max_length=128, unique=True)
    name = models.CharField(verbose_name='名称', max_length=128, null=True, blank=True)
    icon = models.CharField(verbose_name='ele-icon', max_length=128, null=True, blank=True)
    component = models.CharField(verbose_name='组件地址', max_length=128, null=True, blank=True)
    redirect = models.CharField(verbose_name='重定向地址', max_length=128, null=True, blank=True)
    # orderBy排序项
    hidden = models.BooleanField(verbose_name='是否隐藏菜单', default=False)
    sort = models.IntegerField(default=1, verbose_name="显示排序",
                               null=True, blank=True, help_text="显示排序")
    path = models.CharField(verbose_name='路由地址', null=True, blank=True, max_length=128)

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title}"


class MenuButton(models.Model):
    """
    菜单按钮
    """
    menu = models.ForeignKey(to="rbac.Menu", db_constraint=False, on_delete=models.SET_NULL, null=True,
                             related_name='button')
    title = models.CharField(verbose_name="按钮名称", max_length=128)
    value = models.CharField(verbose_name="权限值", max_length=128)
    api = models.CharField(verbose_name='后端接口地址', max_length=128)
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "PATCH"),
        (4, "DELETE")
    )
    method = models.IntegerField(choices=METHOD_CHOICES, default=0, null=True, blank=True, verbose_name="请求方法")

    # is_button = models.BooleanField(verbose_name='是否为按钮权限', default=False)

    class Meta:
        db_table = "rbac_menu_button"
        verbose_name = "按钮"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title}"


class Role(models.Model):
    '''
    角色表
    '''
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, help_text="Id", verbose_name="Id")

    title = models.CharField(verbose_name="角色名称", max_length=32)
    identifier = models.CharField(verbose_name="角色标识符", max_length=32, unique=True)
    menus = models.ManyToManyField('rbac.Menu', verbose_name="角色所有菜单", db_constraint=False, blank=True)
    permissions = models.ManyToManyField('rbac.MenuButton', verbose_name="角色所有权限", db_constraint=False, blank=True)
    status = models.BooleanField(verbose_name='角色状态', null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name
        ordering = ['id']


class Dept(models.Model):
    '''
    部门表
    '''
    title = models.CharField(verbose_name="部门名称", max_length=32, unique=True)
    parent = models.ForeignKey('self', verbose_name="上级部门", related_name='children_dept', null=True,
                               on_delete=models.CASCADE)
    leader = models.ForeignKey('rbac.User', verbose_name="部门负责人", null=True, on_delete=models.SET_NULL,
                               related_name='manage_dept')
    telephone = models.CharField(verbose_name="部门联系电话", max_length=20, null=True, blank=True)

    sort = models.IntegerField(verbose_name="部门排序", default=0, null=True, blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = verbose_name
        ordering = ['sort']


class Post(models.Model):
    '''
    岗位表
    '''
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, help_text="Id", verbose_name="Id")
    title = models.CharField(verbose_name="岗位名称", max_length=32)
    # code =
    # status = models.BooleanField(verbose_name="岗位状态")
    sort = models.IntegerField(verbose_name="岗位排序", default=0, null=True, blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "岗位"
        verbose_name_plural = verbose_name
        ordering = ['sort']


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        '''
        创建用户
        '''
        if not username or not password:
            raise ValueError('用户名或密码不能为空')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        '''
        创建超级用户,django-admin后台的方法
        '''
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    def avatar_file_path(instance, filename):
        type = filename.split('.')[1]
        return 'avatar/{}'.format(filename)

    def detail_file_path(instance, filename):
        type = filename.split('.')[1]
        return 'detail/{}'.format(filename)

    objects = UserManager()
    username = models.CharField(verbose_name="用户名", max_length=30, unique=True)
    IDCard = models.CharField(verbose_name="身份证号", max_length=18, unique=True, blank=True, null=True)
    name = models.CharField(verbose_name='用户姓名', max_length=128, blank=True, null=True)
    email = models.CharField(verbose_name='邮件地址', max_length=100, blank=True, null=True)
    phone = models.CharField(verbose_name="手机号码", max_length=11, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_file_path, verbose_name='个人照片', blank=True, null=True)
    GENDER_CHOICES = (
        (0, "女"),
        (1, "男"),
    )
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1, verbose_name='性别', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='用户状态', default=True)
    is_admin = models.BooleanField(verbose_name='是否为管理员', default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    dept = models.ForeignKey('rbac.Dept', verbose_name="所属部门", on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='belong_dept')
    role = models.ManyToManyField('rbac.Role', verbose_name="关联角色", db_constraint=False)
    post = models.ForeignKey('rbac.Post', verbose_name="所属岗位", on_delete=models.SET_NULL, blank=True, null=True)
    detail = models.FileField(upload_to=detail_file_path, verbose_name="更多信息", blank=True, null=True)

    USERNAME_FIELD = 'username'  # 用户标识符

    # REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # django-admin后台的命令
        return self.is_admin

    class Meta:
        # 元数据
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ['id']


@receiver(pre_delete, sender=User)
def avatar_delete(sender, instance, **kwargs):
    instance.avatar.delete(False)


@receiver(post_init, sender=User)
def file_path(sender, instance, **kwargs):
    instance._current_file = instance.avatar


@receiver(post_save, sender=User)
def delete_old_avatar(sender, instance, **kwargs):
    if hasattr(instance, '_current_file'):
        if instance._current_file != instance.avatar:
            instance._current_file.delete(save=False)


class userFace(models.Model):
    """
    人脸数据库
    """

    def file_path(instance, filename):
        type = filename.split('.')[1]
        return 'face/{}/{}.{}'.format(instance.user.id, uuid.uuid4(), type)

    face = models.ImageField(upload_to=file_path, verbose_name="人脸照片", blank=True, null=True)
    user = models.ForeignKey('rbac.User', verbose_name="人脸所属用户", on_delete=models.CASCADE, related_name="faces")

    class Meta:
        verbose_name = "人脸数据"
        ordering = ['user']


@receiver(pre_delete, sender=userFace)
def face_delete(sender, instance, **kwargs):
    instance.face.delete(False)


@receiver(post_init, sender=userFace)
def file_path(sender, instance, **kwargs):
    instance._current_file = instance.face


@receiver(post_save, sender=userFace)
def delete_old_face(sender, instance, **kwargs):
    if hasattr(instance, '_current_file'):
        if instance._current_file != instance.face:
            instance._current_file.delete(save=False)



