from django.db import transaction

# Create your views here
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_framework.decorators import api_view, permission_classes
from utils.response import APIResponse
from utils.viewset import customModelViewSet
from .serializers import *
from rest_framework.views import APIView
import xlrd

# class CustomPageNumberPagination(PageNumberPagination):
#     """
#     自定义分页器
#     """
#     page_size = 5  # 默认为5
#     page_query_param = 'page'
#     page_size_query_param = 'size'
#     max_page_size = 20
from utils.permissions import CustomPermission



class MenuViewSet(customModelViewSet):
    # authentication_classes = []
    # permission_classes = []
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_Menu_Button(self, request):
        all_menus = Menu.objects.all()
        all_buttons = MenuButton.objects.all()
        root_menus = all_menus.filter(parent=None)
        serializer = MenuButtonTreeSerializer(instance=root_menus, many=True, context={'role_menus': all_menus,
                                                                                       'role_buttons': all_buttons})
        menu_list = serializer.data
        return APIResponse(code=200, msg='获取全部的菜单和按钮成功', data={'menu_list': menu_list})


class ButtonViewSet(customModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = MenuButton.objects.all()
    serializer_class = ButtonSerializer

    def get_buttonByMenuID(self, request):
        menu_id = request.data['menu_id']
        menu = Menu.objects.get(id=menu_id)
        button_list = menu.button
        serializer = self.get_serializer(instance=button_list, many=True)
        return APIResponse(code=200, msg='获取菜单按钮成功', data=serializer.data)


class ImportUser(APIView):
    """
    批量导入用户，并存入数据库中
    """
    permission_classes = []

    def post(self, request):
        gender_dict = {'男': 1, '女': 0}
        status_dict = {'启用': 1, '禁用': 0}
        # 获取用户文件

        file = request.FILES.get('users_file')
        if file is None:
            raise ValueError('请上传用户文件')
        excel_type = file.name.split('.')[1]
        if excel_type not in ['xls', 'xlsx']:
            return APIResponse(code=400, msg='导入用户数据失败')
        # 解析工作表
        wb = xlrd.open_workbook(filename=None, file_contents=file.read())
        # wb = openpyxl.load_workbook(file)
        table = wb.sheets()[0]  # 可迭代列表
        nrows = table.nrows
        try:
            with transaction.atomic():
                sql_list = []
                for i in range(1, nrows):
                    row_value = table.row_values(i)
                    user = User(username=row_value[0], password=make_password(row_value[2]), name=row_value[1],
                                IDCard=row_value[3], phone=row_value[5],
                                gender=gender_dict[row_value[4]], email=row_value[6],
                                is_active=status_dict[row_value[7]])
                    if User.objects.filter(username=user.username).exists():
                        continue
                    sql_list.append(user)
                User.objects.bulk_create(sql_list)
        except Exception as e:
            return APIResponse(code=400, msg=str(e))
        return APIResponse(code=200, msg='导入用户数据成功')


class customUserViewSet(customModelViewSet):
    queryset = User.objects.exclude(is_admin=True)
    serializer_class = userSerializer

    create_serializer_class = userCreateSerializer
    update_serializer_class = userUpdateSerializer
    filter_fields = ('is_active', 'role')
    search_fields = ['username', 'name', 'phone']

    def get_user_info(self, request):
        """
        获取用户的用户名，id，头像等等
        """
        user = request.user
        roles = user.role.all()
        serializer = UserInfoSerializer(user, context={"request": request})
        return APIResponse(data=serializer.data)

    @swagger_auto_schema(
        operation_summary='用户菜单',
        operation_description='获取该用户的所有菜单',
        responses={
            status.HTTP_200_OK: MenuTreeSerializer}
    )
    def get_menus(self, request):
        user = request.user
        # 用户所有的角色
        roles = user.role.all()
        # 菜单列表全部菜单
        root_menus = Menu.objects.none()
        menus = Menu.objects.none()
        for role in roles:
            '''
            找到所有角色的一级菜单
            '''
            menus = menus | role.menus.all()
            root_menus = root_menus | role.menus.filter(parent=None)
        root_menus = root_menus.distinct().order_by('sort')
        menus = menus.distinct().order_by('sort')
        serializer = MenuTreeSerializer(instance=root_menus, many=True, context={'menus': menus})
        return APIResponse(code=200, msg='获取用户菜单成功', data=serializer.data)

    def get_menu_button(self, request):
        user = request.user
        roles = user.role.all()
        # m_id = request.data['menu_id']
        menus = Menu.objects.none()

        button_list = MenuButton.objects.none()
        for each in roles:
            menus = menus | each.menus.all()
            button_list = button_list | each.permissions.all()
        menu_list = []
        for each in menus:
            bs = button_list.distinct().filter(menu=each)
            serializer = MenuButtonSerializer(instance=bs, many=True)
            menu_list.append({'id': each.id,
                              'title': each.title,
                              'button_list': serializer.data
                              })
        return APIResponse(code=200, msg='获取权限成功', data={'menu_list': menu_list})

    def import_user(self, request):
        gender_dict = {'男': 1, '女': 0}
        status_dict = {'启用': 1, '禁用': 0}
        # 获取用户文件

        file = request.FILES.get('users_file')
        if file is None:
            raise ValueError('请上传用户文件')
        excel_type = file.name.split('.')[1]
        if excel_type not in ['xls', 'xlsx']:
            return APIResponse(code=400, msg='导入用户数据失败')
        # 解析工作表
        wb = xlrd.open_workbook(filename=None, file_contents=file.read())
        # wb = openpyxl.load_workbook(file)
        table = wb.sheets()[0]  # 可迭代列表
        nrows = table.nrows
        try:
            with transaction.atomic():
                sql_list = []
                for i in range(1, nrows):
                    row_value = table.row_values(i)
                    user = User(username=row_value[0], password=make_password(row_value[2]), name=row_value[1],
                                IDCard=row_value[3], phone=row_value[5],
                                gender=gender_dict[row_value[4]], email=row_value[6],
                                is_active=status_dict[row_value[7]])
                    if User.objects.filter(username=user.username).exists():
                        continue
                    sql_list.append(user)
                User.objects.bulk_create(sql_list)
        except Exception as e:
            return APIResponse(code=400, msg=str(e))
        return APIResponse(code=200, msg='导入用户数据成功')

    def export_user(self, request):
        keys = request.data['keys']
        if keys is None:
            raise KeyError('请选择需要导出的用户')
        if keys == 'all':
            users = User.objects.exclude(is_admin=True)
        else:
            users = self.get_queryset().filter(id__in=keys)
        serializer = userSerializer(users, many=True)
        response = APIResponse(code=200, msg='导出用户数据成功', data=serializer.data)
        return response


class userFaceViewSet(customModelViewSet):
    queryset = userFace.objects.all()
    serializer_class = userFaceSerializer
    authentication_classes = []
    permission_classes = []
    filter_fields = ()

    def get_facesByID(self, request):
        """获取用户的全部人脸信息"""
        uid = request.data['uid']
        user = User.objects.get(id=uid)
        faces = user.faces.all()
        serializer = retrieveUserFaceSerializer(instance=faces, many=True, context={'request': request})
        return APIResponse(code=200, msg="获取用户人脸信息成功", data=serializer.data)


class DeptViewSet(customModelViewSet):
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    authentication_classes = []

    permission_classes = []

    def get_dept_tree(self, request):
        depts = Dept.objects.all()
        root = Dept.objects.filter(parent=None)
        serializer = DeptTreeSerializer(instance=root, many=True, context={'depts': depts})
        return APIResponse(code=200, msg='获取部门树成功', data=serializer.data)


class PostViewSet(customModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class RoleViewSet(customModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = []
    permission_classes = []

    def get_Menu_Button_ByRoleID(self, request):
        role_id = request.data['role_id']
        role = Role.objects.get(id=role_id)
        role_menus = role.menus.all()
        role_buttons = role.permissions.all()
        serializer = RolePermissionTreeSerializer(instance=role, context={'role_menus': role_menus,
                                                                          'role_buttons': role_buttons})
        return APIResponse(code=200, msg='获取角色的菜单和按钮成功', data=serializer.data)
