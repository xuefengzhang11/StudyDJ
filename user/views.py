from django.http import HttpResponse, JsonResponse
import uuid
from qiniu import Auth

from . import models
import random
from utils.auth import MyAuth


# 用户登录(电话号码或者邮箱登录) user表
# tel_email pwd
# 前后端验证用户名格式
# 后端验证用户是否注册、用户名或密码是否错误
def login(request):
    res = None
    if request.method == 'POST':
        tel_email = request.POST['tel_email']
        pwd = request.POST['pwd']
        res = MyAuth().authenticate(tel_email, pwd)
        res['tel_email'] = tel_email
        return JsonResponse(res)


# 用户注册(手机号注册)
def register(request):
    res = None
    if request.method == 'POST':
        tel = request.POST['tel']
        pwd = request.POST['pwd']
        validate = request.POST['validate']
        # res = regist(tel, pwd, validate)
        return JsonResponse({"res": res})


# 个人信息页(通过手机号码获取用户信息)
def getUser(request, usertel):
    uu = models.userdetail.objects.filter(telephone=usertel).values(
        'name', 'gender__name', 'job__name', 'introduce', 'icon__iconurl', 'city', 'birthday'
    )
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


# 用户随机更换头像
def randomIcon(request):
    allicon = models.icon.objects.all().values_list('iconurl')
    # 随机数据库icon表中的用户头像
    usericon = list(allicon)[random.randint(0, len(allicon))][0]
    return JsonResponse({"userIcon": usericon})


# 用户登录随机获取验证码图片
def randomValidate(request):
    # 获取所有验证码图片路径
    allpics = models.validate.objects.all().values_list('name', 'url')
    # 随机一个
    onepic = list(allpics)[random.randint(0, len(allpics))]
    return JsonResponse({"validateIcon": onepic})


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


# 测试方法
def test(request):
    if request.method == 'POST':
        token = request.POST['token']
        res = MyAuth().identify(token)
        return HttpResponse('测试路由')
