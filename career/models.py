from django.db import models


class career(models.Model):
    name = models.CharField(max_length=100)
    introduce = models.CharField(max_length=255)
    price = models.FloatField(null=False, default=0)
    learn = models.IntegerField(null=False, default=0)
    imgurl = models.CharField(max_length=100, null=True)
    finish = models.CharField(max_length=255)

