from django.db import models


# 课程表
class course(models.Model):
    name = models.CharField(max_length=50)
    introduce = models.CharField(max_length=255, null=True)
    price = models.FloatField(null=False, default=0)
    learn = models.IntegerField(null=True, default=0)
    imgurl = models.CharField(max_length=100)
    # cs_categry_id 为 course_category 表中主键id
    cs_category = models.ForeignKey(to='category', to_field='id', on_delete=True)
    # cs_direction_id 为 course_direction 表中主键id
    cs_direction = models.ForeignKey(to='direction', to_field='id', on_delete=True)
    # cs_degree_id 为 course_degree 表中主键id
    cs_degree = models.ForeignKey(to='degree', to_field='id', on_delete=True)
    # cs_career_id 为 career_carer 表中主键id
    cs_career = models.ForeignKey(to='career.career', null=True, to_field='id', on_delete=True)


# 课程章表
class chapter(models.Model):
    name = models.CharField(max_length=50)
    introduce = models.CharField(max_length=255)
    upload = models.DateTimeField()
    course = models.ForeignKey(to='course', to_field='id', on_delete=True)


# 课程节表
class section(models.Model):
    name = models.CharField(max_length=100)
    introduce = models.CharField(max_length=255, null=True)
    upload = models.DateTimeField()
    chapter = models.ForeignKey(to='chapter', to_field='id', on_delete=True)


# 课程收藏表
class collection(models.Model):
    collecttime = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(to='course', to_field='id', on_delete=True)
    user = models.ForeignKey(to='user.user', to_field='id', on_delete=True)


# 课程的观看历史纪录
class history(models.Model):
    watchtime = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey(to='section', to_field='id', on_delete=True)
    user = models.ForeignKey(to='user.user', to_field='id', on_delete=True)


# 课程方向表
class direction(models.Model):
    name = models.CharField(max_length=30)


# 课程分类表
class category(models.Model):
    name = models.CharField(max_length=30)
    # 外键ctgr_direction_id 为 direction 表中主键id
    ctgr_direction = models.ForeignKey(to="direction", to_field="id", on_delete=True)


# 课程难度表
class degree(models.Model):
    name = models.CharField(max_length=30)
