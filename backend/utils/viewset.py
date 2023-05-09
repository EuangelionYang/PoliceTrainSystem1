# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from utils.response import APIResponse


class CustomModelViewSet(ModelViewSet):
    """自定义的类视图"""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.isvalid(raise_exception=True)
        self.perform_create(serializer)
        return APIResponse(data=serializer.data)


class customModelViewSet(ModelViewSet):
    """
    自定义的ModelViewSet:
    统一标准的返回格式;新增,查询,修改可使用不同序列化器
    (1)ORM性能优化, 尽可能使用values_queryset形式
    (2)create_serializer_class 新增时,使用的序列化器
    (3)update_serializer_class 修改时,使用的序列化器
    """
    values_queryset = None
    ordering_fields = '__all__'
    create_serializer_class = None
    update_serializer_class = None
    filter_fields = ()
    search_fields = ()
    # extra_filter_backends = [DataLevelPermissionsFilter]
    extra_filter_backends = []

    # permission_classes = [CustomPermission]

    def filter_queryset(self, queryset):
        for backend in set(set(self.filter_backends) | set(self.extra_filter_backends or [])):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        """
        values_queryset是queryset的部分字段
        """
        if getattr(self, 'values_queryset', None):
            return self.values_queryset
        return super().get_queryset()

    def get_serializer_class(self):
        action_serializer_name = f"{self.action}_serializer_class"
        action_serializer_class = getattr(self, action_serializer_name, None)
        if action_serializer_class:
            return action_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return APIResponse(data=serializer.data, msg="新增成功")

    def list(self, request, *args, **kwargs):
        no_page = request.query_params.get('no_page',None)
        # limit = int(request.query_params['limit'])
        queryset = self.filter_queryset(self.get_queryset())
        # print(no_page)
        if no_page is None:
            page = self.paginate_queryset(queryset)
        else:
            page = None
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return APIResponse(data=serializer.data, msg="获取成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, request=request)
        return APIResponse(data=serializer.data, msg="获取成功")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, request=request, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return APIResponse(data=serializer.data, msg="更新成功")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return APIResponse(data=[], msg="删除成功")

    keys = openapi.Schema(description='主键列表', type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['keys'],
        properties={'keys': keys}
    ), operation_summary='批量删除')
    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        request_data = request.data
        # print(type(request_data))
        # 通过getlist取列表
        keys = request_data.get('keys', None)
        if keys:
            self.get_queryset().filter(id__in=keys).delete()
            return APIResponse(data=[], msg="删除成功")
        else:
            return APIResponse(code='400', msg="未获取到keys字段")
