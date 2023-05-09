"""PoliceTrainSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import token_refresh
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import settings
from rbac.utils import LoginView, resetPasswordView, LoginSerializer, LogoutView, FaceIDView, updatePasswordView

schema_view = get_schema_view(
    openapi.Info(

        title='执法训练管理平台',
        default_version='v1.0',
        description='后端接口文档',
    ),

    authentication_classes=(JWTAuthentication,),
    public=True,
    permission_classes=(permissions.AllowAny,)
)
# decorated_login_view = \
#     swagger_auto_schema(
#         method='post',
#         responses={status.HTTP_200_OK: LoginSerializer}
#     )(LoginView.as_view())
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('user/', include('user.urls')),  # user下的路由交给user.urls处理
    re_path('^api/rbac/', include('rbac.urls', namespace='rbac')),
    re_path('^api/training/', include('apps.training.urls')),

    # re_path('^api/lesson/', include('apps.lesson.urls')),
    re_path('^api/login/$', LoginView.as_view(), name='login'),
    re_path('^api/logout/$', LogoutView.as_view(), name='logout'),
    re_path('^api/reset_password/$', resetPasswordView.as_view()),
    re_path('^api/update_password/$', updatePasswordView.as_view()),
    re_path('^api/refresh/$', token_refresh),
    # 获取资源接口
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # swag后台路由
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api_doc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^api/faceid/$',FaceIDView.as_view(),name='FaceID'),
]
