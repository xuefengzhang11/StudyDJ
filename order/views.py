from django.http import HttpResponse, JsonResponse

from . import models
from user.models import user


# Create your views here.

# 判断用户是否购买这门课程
def isBuy(request, courid, usertel):
    res = judgeBuy(courid, usertel)
    return JsonResponse({"res": res})

# 判断是否购买方法
def judgeBuy(courid, usertel):
    uid = user.objects.get(telephone=usertel).id
    count = models.order.objects.filter(course_id=courid, user_id=uid, status_id=1)
    if count:
        res = '已购买'
    else:
        res = '未购买'
    return res

# 加入购物车
def joincart(request, courid, usertel):
    res = judgeBuy(courid, usertel)
    if res == '未购买':
        uid = user.objects.get(telephone=usertel).id
        count = models.coursecat.objects.filter(course_id=courid, user_id=uid)
        if count:
            res = '不能重复添加'
        else:
            models.coursecat.objects.create(course_id=courid, user_id=uid)
            res = '添加成功'
    return JsonResponse({"res": res})