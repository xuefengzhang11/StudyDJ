from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import user


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
        return JsonResponse({"结果": res})

# 邮箱登录
def loginEmail(email, pwd):
    uu = user.objects.filter(email=email)
    if uu:
        if uu[0].password == pwd:
            res = '登录成功'
        else:
            res = '用户邮箱或密码错误'
        pass
    else:
        res = '该用户未注册'
    return res

# 电话登录
def loginTel(tel, pwd):
    uu = user.objects.filter(telephone=tel)
    if uu:
        if uu[0].password == pwd:
            res = '登录成功'
        else:
            res = '电话号或密码错误'
        pass
    else:
        res = '该用户未注册'
    return res



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
