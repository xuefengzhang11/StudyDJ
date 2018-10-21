from django.db import models


# 文章表
class article(models.Model):
    title = models.CharField(max_length=50)
    introduce = models.CharField(max_length=255)
    content = models.TextField()
    upload = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(null=False, default=0)
    userinfo = models.ForeignKey(to='user.userdetail', to_field='id', on_delete=True)


# 文章点赞表
class article_like(models.Model):
    article = models.ForeignKey(to='article', to_field='id', on_delete=True)
    user = models.ForeignKey(to='user.userdetail', to_field='id', on_delete=True)


# 文章收藏表
class article_collection(models.Model):
    collecttime = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(to='article', to_field='id', on_delete=True)
    userinfo = models.ForeignKey(to='user.userdetail', to_field='id', on_delete=True)

# 文章评论表
class comment(models.Model):
    content = models.CharField(max_length=255)
    uptime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to='user.userdetail', to_field='id', on_delete=True)
    article = models.ForeignKey(to='article', to_field='id', on_delete=True)

# 评论点赞表
class comment_like(models.Model):
    comment = models.ForeignKey(to='comment', to_field='id', on_delete=True)
    user = models.ForeignKey(to='user.userdetail', to_field='id', on_delete=True)

# 评论评论表
class comment_comment(models.Model):
    content = models.CharField(max_length=255)
    uptime = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(to='comment', to_field='id', on_delete=True)
    user = models.ForeignKey(to='user.userdetail', to_field='id', on_delete=True)