# 系统模块
from django.http import JsonResponse
import json, time
from datetime import datetime
# 自定义模块
from . import models
from user.models import user, userdetail
from course.models import course
from utils.randomOrderNum import getordernumber


# 判断用户是否购买这门课程
def isBuy(request, courid, usertel):
    res = judgeBuy(courid, usertel)
    return JsonResponse({"res": res})


# 判断是否购买方法
def judgeBuy(courid, usertel):
    uid = user.objects.get(telephone=usertel).id
    count = models.order.objects.filter(course_id=courid, user_id=uid, status_id=1)
    res = '已购买' if count else '未购买'
    return res


# 加入购物车
def joincart(request, courid, usertel):
    try:
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
    except Exception as e:
        print(e)
        return JsonResponse({"res": 409})


# 查询订单信息
def getStatusOrder(request, usertel, status):
    try:
        failureOrder(usertel)
        uid = user.objects.get(telephone=usertel).id
        res = []
        if status == '1' or status == '2' or status == '3':
            orders = models.order.objects.filter(user_id=uid, status_id=status).values()
            uname = user.objects.filter(id=uid).values('name')
            for ord in list(orders):
                ucourse = course.objects.filter(id=ord['course_id']).values('name', 'price','imgurl')
                ustatus = models.status.objects.filter(id=ord['status_id']).values('name')
                ord['user_name'] = uname[0]['name']
                ord['course_name'] = ucourse[0]['name']
                ord['course_price'] = ucourse[0]['price']
                ord['status_name'] = ustatus[0]['name']
                ord['imgurl'] = ucourse[0]['imgurl']
                res.append(ord)
        elif status == '4':
            orders = models.order.objects.filter(user_id=uid).values()
            uname = user.objects.filter(id=uid).values('name')
            for ord in list(orders):
                ucourse = course.objects.filter(id=ord['course_id']).values('name', 'price','imgurl')
                ustatus = models.status.objects.filter(id=ord['status_id']).values('name')
                ord['user_name'] = uname[0]['name']
                ord['course_name'] = ucourse[0]['name']
                ord['course_price'] = ucourse[0]['price']
                ord['status_name'] = ustatus[0]['name']
                ord['imgurl'] = ucourse[0]['imgurl']
                res.append(ord)

        return JsonResponse({"orders": res}, json_dumps_params={'ensure_ascii': False})
    except Exception as ex:
        print(ex)
        return JsonResponse({"res": 409})


# 查询用户购物车,根据用户电话号码
# 查询加入购物车信息
def getCourCarts(request, usertel):
    try:
        uid = user.objects.get(telephone=usertel).id
        carts = models.coursecat.objects.filter(user_id=uid).values()
        uname = user.objects.filter(id=uid).values('name')
        res = []
        for cart in list(carts):
            ucourse = course.objects.filter(id=cart['course_id']).values(
                'id', 'name', 'price', 'imgurl', 'coursecat__checked')[0]
            ucourse['cartid'] = cart['id']
            res.append(ucourse)
        return JsonResponse({"carts": res}, json_dumps_params={'ensure_ascii': False})
    except Exception as ex:
        print(ex)
        return JsonResponse({"res": 409})


# 通过id删除购物车数据
def delCartById(request, cartid):
    try:
        models.coursecat.objects.filter(id=cartid).delete()
        return JsonResponse({"res": '删除成功'})
    except Exception as e:
        print(e)
        return JsonResponse({"res": '删除失败'})


# 全选或者全不选
def choiceAllOrNot(request, flag, usertel):
    try:
        uid = userdetail.objects.get(telephone=usertel).id
        models.coursecat.objects.filter(user_id=uid).update(checked=flag)
    except Exception as e:
        print(e)
        return JsonResponse({"res": '失败'})
    return JsonResponse({"res": '成功'})


# 单个选择或取消
def ChangeCartById(request, cartid, usertel):
    try:
        uid = userdetail.objects.get(telephone=usertel).id
        nowFlag = models.coursecat.objects.get(user_id=uid, id=cartid).checked
        models.coursecat.objects.filter(user_id=uid, id=cartid).update(checked=not nowFlag)
    except Exception as e:
        print(e)
        return JsonResponse({"res": '修改失败'})
    return JsonResponse({"res": '修改成功'})


# 确认购买
def goBuy(request, usertel):
    try:
        uid = userdetail.objects.get(telephone=usertel).id
        carts = json.loads(request.body.decode())
        for cart in carts:
            if cart['checked']:
                # 购买 删除购物车信息
                models.coursecat.objects.get(course_id=cart['id']).delete()
                # 添加到订单表中(生成订单编号)
                models.order.objects.create(number=getordernumber(), course_id=cart['id'], status_id=1, user_id=uid)
    except Exception as e:
        print(e)
        return JsonResponse({"res": '失败'})
    return JsonResponse({"res": '成功'})


# 取消购买
def noBuy(request, usertel):
    try:
        uid = userdetail.objects.get(telephone=usertel).id
        carts = json.loads(request.body.decode())
        for cart in carts:
            if cart['checked']:
                # 购买 删除购物车信息
                models.coursecat.objects.get(course_id=cart['id'], user_id=uid).delete()
                # 添加到订单表中(生成订单编号)
                models.order.objects.create(number=getordernumber(), course_id=cart['id'], status_id=2, user_id=uid)
        return JsonResponse({"res": '成功'})
    except Exception as e:
        print(e)
        return JsonResponse({"res": '失败'})


# 删除订单
def deleteOrder(request, orderid):
    try:
        delete_order = models.order.objects.filter(id=orderid).delete()
        res = '删除成功' if delete_order[0] else '删除失败'
        return JsonResponse({"res": res})
    except Exception as ex:
        print(ex)


# 过三天 判定为失效
def failureOrder(tel):
    userid = userdetail.objects.get(telephone=tel).id
    shop_time = models.order.objects.filter(user_id=userid).values('ordertime')
    for st in list(shop_time):
        st_time1 = str(st['ordertime']).split('+')[0]
        st_time2 = st_time1.split('.')[0]
        # string转化结构化时间
        time_array = time.strptime(st_time2, "%Y-%m-%d %H:%M:%S")
        # 结构化时间转时间戳
        timestamp = time.mktime(time_array)
        ntime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        now_time = time.strptime(ntime, "%Y-%m-%d %H:%M:%S")
        nowtime = time.mktime(now_time)
        if nowtime - 24 * 60 * 60 * 3 > timestamp:
            now_status = models.order.objects.filter(ordertime=st['ordertime']).update(status_id=3)
