from django.db import models


# 文章表
class article(models.Model):
    title = models.CharField(max_length=50)
    introduce = models.CharField(max_length=255)
    content = models.TextField()
    upload = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(null=False, default=0)
    userinfo = models.ForeignKey(to='user.userdetail', to_field='id', on_delete=True)


# 文章收藏表
class article_collection(models.Model):
    collecttime = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(to='article', to_field='id', on_delete=True)
    userinfo = models.ForeignKey(to='user.userdetail', to_field='id', on_delete=True)
