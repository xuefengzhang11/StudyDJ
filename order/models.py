from django.db import models


# 订单表
class order(models.Model):
    # 订单编号
    number = models.CharField(max_length=100)
    ordertime = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(to='status', to_field='id', on_delete=True)
    course = models.ForeignKey(to='course.course', to_field='id', on_delete=True)
    user = models.ForeignKey(to='user.user', to_field='id', on_delete=True)


# 订单状态表
class status(models.Model):
    name = models.CharField(max_length=20)


# 购物车表
class coursecat(models.Model):
    jointime = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(null=False, default=False)
    course = models.ForeignKey(to_field='id', to='course.course', on_delete=True)
    user = models.ForeignKey(to_field='id', to='user.userdetail', on_delete=True)
