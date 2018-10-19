from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import models
import json


# 用户登录(电话号码或者邮箱登录) user表
# tel_email pwd
# 前后端验证用户名格式
# 后端验证用户是否注册、用户名或密码是否错误
def login(request):
    res = None
    if request.method == 'POST':
        tel_email = request.POST['tel_email']
        pwd = request.POST['pwd']
        if str(tel_email).find('@') != -1:
            # 邮箱登录
            res = loginEmail(tel_email, pwd)
        else:
            # 电话号码登录
            res = loginTel(tel_email, pwd)
        return JsonResponse({"res": res})


# 邮箱登录
def loginEmail(email, pwd):
    uu = models.user.objects.filter(email=email)
    if uu:
        if uu[0].password == pwd:
            res = '登录成功', uu[0].telephone
        else:
            res = '用户邮箱或密码错误'
        pass
    else:
        res = '该用户未注册'
    return res


# 电话登录
def loginTel(tel, pwd):
    uu = models.user.objects.filter(telephone=tel)
    if uu:
        if uu[0].password == pwd:
            res = '登录成功', uu[0].telephone
        else:
            res = '电话号或密码错误'
        pass
    else:
        res = '该用户未注册'
    return res


# 用户注册
def register(request):
    res = None
    if request.method == 'POST':
        tel = request.POST['tel']
        pwd = request.POST['pwd']
        validate = request.POST['validate']
        res = regist(tel, pwd, validate)

        return JsonResponse({"res": res})


# 注册方法
def regist(tel, pwd, validate):
    pass


# 个人信息页(通过手机号码获取用户信息)
def getUser(request, usertel):
    uu = models.userdetail.objects.filter(telephone=usertel).values(
        'name','gender__name','job__name','introduce','icon__iconurl','city','birthday'
    )
    print(uu)
    return JsonResponse({"user": list(uu)}, json_dumps_params={'ensure_ascii': False})


# 个人设置页
def set(request):
    return HttpResponse('个人设置页')


# 修改用户信息
def update(request):
    return HttpResponse('修改用户信息')


