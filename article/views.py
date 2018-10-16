from django.shortcuts import render
from django.http import JsonResponse
from .models import article
from django.forms import model_to_dict


def hotArticle(request):
    arts = []
    articles = article.objects.all().order_by('-like')
    for art in articles:
        art_dict = model_to_dict(art)
        # 获取用户头像
        art_dict['user_img'] = art.userinfo.icon.iconurl
        # 获取用户昵称
        art_dict['user_name'] = art.userinfo.name
        art_dict['upload'] = art.upload.strftime("%Y-%m-%d")
        arts.append(art_dict)
    return JsonResponse({"articles": arts}, json_dumps_params={'ensure_ascii': False})


# 根据ID得到文章信息
def getArticle(request, id):
    art = article.objects.get(id=id)
    art_dict = model_to_dict(art)
    art_dict['upload'] = art.upload.strftime("%Y-%m-%d %H:%M:%S")
    # 获取用户信息
    user = art.userinfo
    user_dict = model_to_dict(user)
    user_dict['user_job'] = user.job.name
    user_dict['user_img'] = user.icon.iconurl
    return JsonResponse({"article": art_dict, "user": user_dict}, json_dumps_params={'ensure_ascii': False})

