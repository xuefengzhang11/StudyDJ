from django.http import HttpResponse, JsonResponse

from . import models
from user.models import user
from course.models import course


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

# 查询订单信息
def getStatusOrder(request,usertel,status):
    try:
        uid = user.objects.get(telephone=usertel).id
        res = []
        if status == '1' or status == '2' or status == '3':
            orders = models.order.objects.filter(user_id=uid, status_id=status).values()
            uname = user.objects.filter(id=uid).values('name')
            for ord in list(orders):
                ucourse = course.objects.filter(id=ord['course_id']).values('name', 'price')
                ustatus = models.status.objects.filter(id=ord['status_id']).values('name')
                ord['user_name'] = uname[0]['name']
                ord['course_name'] = ucourse[0]['name']
                ord['course_price'] = ucourse[0]['price']
                ord['status_name'] = ustatus[0]['name']
                res.append(ord)
        elif status == '4':
            orders = models.order.objects.filter(user_id=uid).values()
            uname = user.objects.filter(id=uid).values('name')
            for ord in list(orders):
                ucourse = course.objects.filter(id=ord['course_id']).values('name', 'price')
                ustatus = models.status.objects.filter(id=ord['status_id']).values('name')
                ord['user_name'] = uname[0]['name']
                ord['course_name'] = ucourse[0]['name']
                ord['course_price'] = ucourse[0]['price']
                ord['status_name'] = ustatus[0]['name']
                res.append(ord)

        return JsonResponse({"orders": res}, json_dumps_params={'ensure_ascii': False})
    except Exception as ex:
        print(ex)



# 查询用户购物车,根据用户电话号码
# 查询加入购物车信息
def getCourCarts(request,usertel):
    try:
        uid = user.objects.get(telephone=usertel).id
        carts = models.coursecat.objects.filter(user_id=uid).values()
        uname=user.objects.filter(id=uid).values('name')
        res=[]
        for cart in list(carts):
            ucourse = course.objects.filter(id=cart['course_id']).values('id','name','price','imgurl','coursecat__checked')
            res.append(ucourse[0])
        print(res)
        return JsonResponse({"carts": res}, json_dumps_params={'ensure_ascii': False})
    except Exception as ex:
        print(ex)