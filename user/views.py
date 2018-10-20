from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import models
import json
import uuid
from qiniu import Auth


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
        'name', 'gender__name', 'job__name', 'introduce', 'icon__iconurl', 'city', 'birthday'
    )
    print(uu)
    return JsonResponse({"user": list(uu)}, json_dumps_params={'ensure_ascii': False})


# 个人设置页
def set(request):
    return HttpResponse('个人设置页')


# 修改用户信息
def update(request):
    return HttpResponse('修改用户信息')


# 用户上传头像（保存头像文件名称）（更改用户头像）
def upIcon(request, fname, tel):
    try:
        obj = models.icon.objects.create(iconurl=fname)
        # 当前插入图片的ID为obj.id
        # 修改用户的头像
        count = models.userdetail.objects.filter(telephone=tel).update(icon_id=obj.id)
        return JsonResponse({"res": "修改成功"}, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        print(e)
        return JsonResponse({"res": "修改失败"}, json_dumps_params={'ensure_ascii': False})


# 七牛云token
def sendToken(request):
    if request.method == 'GET':
        access_key = 'uFy_2nTo_c-fCDvigBum8ZnwvFZPwRceTAbw7zVS'
        secret_key = '6rGh9INqH0vQWj4BXc0yEfPsz1dLyvUk0H8JtNPe'
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = 'studyapp'
        # 上传到七牛后保存的文件名
        key = str(uuid.uuid4()) + '.' + str(request.GET.get('key')).split('.')[-1]
        # 生成上传 Token，可以指定过期时间等 一天
        token = q.upload_token(bucket_name, key, 3600)

        return JsonResponse({"token": token, "filename": key})
