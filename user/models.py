from django.db import models


# 用户基本表
class user(models.Model):
    telephone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    role = models.CharField(null=False, default='user', max_length=20)
    register = models.DateTimeField(auto_now_add=True)


# 用户详情表
class userdetail(models.Model):
    name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    birthday = models.DateField()
    city = models.CharField(max_length=100)
    introduce = models.CharField(max_length=200)
    gender = models.ForeignKey(to='gender', to_field='id', on_delete='True')
    icon = models.ForeignKey(to='icon', to_field='id', on_delete=True)
    job = models.ForeignKey(to='job', to_field='id', on_delete=True)


# 用户头像
class icon(models.Model):
    iconurl = models.CharField(max_length=200)


# 用户性别表
class gender(models.Model):
    name = models.CharField(max_length=10)


# 用户职业表
class job(models.Model):
    name = models.CharField(max_length=20)
