"""studyDJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    # 导入子模块
    path('user/', include('user.urls', namespace='stu_user')),  # user 模块
    path('course/', include('course.urls', namespace='stu_course')),  # course 模块
    path('career/', include('career.urls', namespace='stu_career')),  # career 模块
    path('article/', include('article.urls', namespace='stu_article')),  # article 模块
    path('order/', include('order.urls', namespace='stu_order')),  # 订单模块

    path('admin/', admin.site.urls),
    # 思达迪首页
    url(r'^$', views.home, name='home')
]
