from django.contrib import admin
from django.urls import path, include, re_path
from app01 import views
from django.conf import settings  # 新增
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),  # 后台管理界面
    path("admin_home/", views.admin_home),  # 后台管理界面主页
    path("", views.index),  # 主页
    path("news/", views.news),  # 新闻界面
    path("search/", views.search),  # 文章搜索
    path("moods/", views.moods),  # 心情界面
    path('history/', views.history),  # 网站历史
    path('sites/', views.sites),  # 网站导航
    path("login/", views.login),  # 登录
    path("login/random_code/", views.get_random_code),  # 验证码
    path("sign/", views.sign),  # 注册
    path("logout/", views.logout),  # 退出登录

    path("backend/", views.backend),  # 后台个人中心
    path("backend/add_article/", views.add_article),  # 添加文章
    path("backend/edit_avatar/", views.edit_avatar),  # 修改头像
    path("backend/reset_password/", views.reset_password),  # 重置密码
    path("backend/cover_list/", views.cover_list),  # 文章封面
    path("backend/avatar_list/", views.avatar_list),  # 头像列表
    re_path(r'^backend/edit_article/(?P<nid>\d+)/', views.edit_article),  # 编辑文章

    re_path(r'^article/(?P<nid>\d+)/', views.article),  # 文章详情页

    re_path(r'^api/', include('api.urls')),  # 路由分发，将所有以api开头的请求全部分发到api这个的urls.py里面

    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 用户上传文件路由配置

    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]
