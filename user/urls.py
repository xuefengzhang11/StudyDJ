from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'user'

urlpatterns = [
    url(r'getUser/(?P<usertel>\w*)', views.getUser, name='getUser'),  # 个人信息页（通过手机号）
    path('set/', views.set, name='set'),  # 个人设置页
    url(r'login', views.login, name='login'),  # 用户登录页
    url(r'register', views.register, name='register'),  # 用户登录页
    url(r'upIcon/(?P<fname>.*?)/(?P<tel>\d*)', views.upIcon, name='upIcon'),  # 用户上传头像

    url(r'qiniutoken/', views.sendToken, name='sendToken')  # 用户上传头像准备工作，签发七牛云token，处理文件名
]
