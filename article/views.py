from django.http import JsonResponse
from .models import article
from .models import article_collection
from django.forms import model_to_dict
from . import models
from user.models import userdetail


# 根据ID得到文章信息
def getArticleById(request, id):
    art = article.objects.get(id=id)
    art_dict = model_to_dict(art)
    art_dict['upload'] = art.upload.strftime("%Y-%m-%d %H:%M:%S")
    # 获取用户信息
    user = art.userinfo
    user_dict = model_to_dict(user)
    user_dict['user_job'] = user.job.name
    user_dict['user_img'] = user.icon.iconurl
    print(art_dict)
    print(user_dict)
    return JsonResponse({"article": art_dict, "user": user_dict}, json_dumps_params={'ensure_ascii': False})


# 根据文章id取出文章作者共写了多少文章和相关文章
def getUserArticle(request, id):
    uu = article.objects.get(id=id).userinfo
    uu_articles = uu.article_set.all().values('id', 'title')[0:3]
    nums = uu.article_set.all().count()
    return JsonResponse({"nums": nums, "uu_articles": list(uu_articles)}, json_dumps_params={'ensure_ascii': False})


# 获取所有文章（多条件筛选分页）
def getArticle(request, con, pageIndex):
    pageSize = 12
    pageIndex = int(pageIndex)
    start = (pageIndex - 1) * pageSize
    end = pageIndex * pageSize
    all_con = {}
    if con:
        all_con['title__icontains'] = con
    try:
        articles = article.objects.filter(**all_con).order_by('id').values(
            'id', 'title', 'introduce', 'upload', 'userinfo__name', 'userinfo__icon__iconurl', 'like')[start:end]
        return JsonResponse({"articles": list(articles)}, json_dumps_params={'ensure_ascii': False})
    except Exception as ex:
        return JsonResponse({"code": "409"})


# 返回的是文章的数量
def acount(request, con):
    try:
        if not con:
            len = models.article.objects.all().count()
        else:
            len = models.article.objects.filter(title__icontains=con).count()
            # len = models.job.objects.filter(title__regex=con).count()
        return JsonResponse({"acount": len})
    except Exception as ex:
        return JsonResponse({"code": "409"})


# 获取热门文章
def hotArticle(request):
    arts = []
    articles = article.objects.all().order_by('-like')[0:4]
    for art in articles:
        art_dict = model_to_dict(art)
        # 获取用户头像
        art_dict['user_img'] = art.userinfo.icon.iconurl
        # 获取用户昵称
        art_dict['user_name'] = art.userinfo.name
        art_dict['upload'] = art.upload.strftime("%Y-%m-%d")
        arts.append(art_dict)
    return JsonResponse({"articles": arts}, json_dumps_params={'ensure_ascii': False})


# 根据用户的tel获取用户收藏的信息
def getCollectArticle(request, tel):
    res = {}
    userid = userdetail.objects.filter(telephone=tel).values('id')
    # uu = userdetail.objects.filter(telephone=tel).values('name')[0]
    # res['user'] = uu
    arts = article_collection.objects.filter(userinfo_id=list(userid)[0]['id']).values('article_id')
    print(arts)
    arti = []
    res['article'] = arti
    for a in range(len(arts)):
        arttitle = article.objects.filter(id = list(arts)[a]['article_id']).order_by('-id').values('id','title','introduce','upload','userinfo__name','like')[0]
        arti.append(arttitle)
    return JsonResponse(res)

 # 删除收藏文章
def deleteArticle(request, id):
    try:
        delete_section = models.article_collection.objects.filter(article_id=id).delete()
        # print(delete_section)
        if delete_section[0]:
            return JsonResponse({"code":"888"})
        else:
            return JsonResponse({"code": "444"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})

# 根据用户的tel获取用户写的文章
def getMyArticle(request, tel):
    res = {}
    userid = userdetail.objects.filter(telephone=tel).values('id')
    # uu = userdetail.objects.filter(telephone=tel).values('name')[0]
    # res['user'] = uu
    arts = article.objects.filter(userinfo_id=list(userid)[0]['id']).values('id')
    print(arts)
    arti = []
    res['article'] = arti
    for a in range(len(arts)):
        arttitle = article.objects.filter(id = list(arts)[a]['id']).order_by('-id').values('id','title','introduce','upload','like')[0]
        arti.append(arttitle)
    return JsonResponse(res)

 # 删除个人文章
def deleteUserArticle(request, id):
    try:
        delete_section = models.article.objects.filter(id=id).delete()
        # print(delete_section)
        if delete_section[0]:
            return JsonResponse({"code":"888"})
        else:
            return JsonResponse({"code": "444"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})