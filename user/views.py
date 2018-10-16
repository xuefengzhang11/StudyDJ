from django.shortcuts import render
from django.http import HttpResponse


# 用户登录
def login(request):
    return HttpResponse('用户登录')


# 用户注册
def register(request):
    return HttpResponse('用户注册')


# 个人信息页
def info(request, userid):
    return HttpResponse('个人信息页' + userid)


# 个人设置页
def set(request):
    return HttpResponse('个人设置页')


# 修改用户信息
def update(request):
    return HttpResponse('修改用户信息')
