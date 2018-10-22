from django.http import HttpResponse, JsonResponse
import uuid, json, time
from qiniu import Auth

from . import models
import random
from utils.auth import MyAuth
from utils.sms_api import sendIndustrySms
from utils.randomUserName import getRandomName


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
        if str(tel_email).find('@') != -1:
            # 通过用户邮箱查找用户电话号码
            res['tel_email'] = models.user.objects.get(email=tel_email).telephone
        else:
            res['tel_email'] = tel_email
        return JsonResponse(res)


# 用户请求发送验证码
def sendValidate(request):
    if request.method == 'POST':
        res = {}
        # 获取用户电话
        user_tel = request.POST['user_tel']
        print(user_tel)
        # 判断是否已经注册
        if not len(models.user.objects.filter(telephone=user_tel)):
            # 验证码过期时间 过期时间五分钟
            expire = 5
            expiretime = int(time.time()) + expire * 60
            # 调用接口，返回状态码respCode，状态信息respDesc，验证码validate
            res = sendIndustrySms(user_tel, expire)
            if res['respCode'] == '00000':
                # 请求成功  存数据库(添加或者更新)
                if len(models.registertemp.objects.filter(telephone=user_tel)):
                    # 修改
                    models.registertemp.objects.filter(telephone=user_tel).update(validate=res['validate'],
                                                                                  expiretime=expiretime)
                else:
                    # 添加
                    models.registertemp.objects.create(telephone=user_tel, validate=res['validate'],
                                                       expiretime=expiretime)
        else:
            res['respDesc'] = '该电话号码已被注册'
        return JsonResponse({"msg": res['respDesc']})


# 用户注册(手机号注册)
def register(request):
    res = None
    token = None
    if request.method == 'POST':
        try:
            tel = request.POST['tel']
            pwd = request.POST['pwd']
            # 随机生成用户昵称
            uname = getRandomName()
            models.user.objects.create(telephone=tel, password=pwd, name=uname)
            res = '注册成功'
            # 获取token
            token = MyAuth.encode_auth_token(tel, int(time.time()))
        except Exception as e:
            res = '注册失败'
            print(e)
        return JsonResponse({"res": res, "token": token})


# 个人信息页(通过手机号码获取用户信息)
def getUser(request, usertel):
    uu = models.userdetail.objects.filter(telephone=usertel).values(
        'name', 'gender__name', 'gender_id', 'job_id', 'job__name', 'introduce', 'icon__iconurl', 'city', 'birthday'
    )
    return JsonResponse({"user": list(uu)}, json_dumps_params={'ensure_ascii': False})


# 个人设置页
def set(request):
    return HttpResponse('个人设置页')


# 修改用户信息
def update(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            name = data['name']
            telephone = data['usertel']
            city = data['city']
            birthday = data['birthday']
            introduce = data['introduce']
            gender__name = data['gender']
            job__name = data['job']
            job_id = None
            uu = models.job.objects.all().values('id', 'name')
            for u in uu:
                if job__name == u['name']:
                    job_id = u['id']

            upuser = models.userdetail.objects.filter(
                telephone=telephone).update(name=name, birthday=birthday, city=city, introduce=introduce,
                                            gender_id=gender__name, job_id=job_id)
            if upuser:
                res = '修改成功'
            else:
                res = '修改失败'

            return JsonResponse({"res": res})
    except Exception as ex:
        print(ex)


# 查找职业
def getjob(request):
    jobs = models.job.objects.all().values()
    return JsonResponse({"job": list(jobs)}, json_dumps_params={'ensure_ascii': False})


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
    onepic = list(allpics)[random.randint(0, len(allpics) - 1)]
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
        return HttpResponse('测试身份鉴定')
