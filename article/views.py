from django.http import JsonResponse
from django.forms import model_to_dict
from django.db.models import F
from . import models
from user.models import userdetail
import json
from datetime import datetime


# 根据ID得到文章信息
def getArticleById(request, id, tel):
    art = models.article.objects.get(id=id)
    art_dict = model_to_dict(art)
    art_dict['upload'] = art.upload.strftime("%Y-%m-%d %H:%M:%S")
    # 获取用户信息
    user = art.userinfo
    user_dict = model_to_dict(user)
    user_dict['user_job'] = user.job.name
    user_dict['user_img'] = user.icon.iconurl
    islike = False
    if tel:
        userid = userdetail.objects.get(telephone=tel).id
        count = models.article_like.objects.filter(user_id=userid, article_id=id).count()
        islike = count == 1 if True else False
    art_dict['like_flag'] = islike
    return JsonResponse({"article": art_dict, "user": user_dict}, json_dumps_params={'ensure_ascii': False})


# 根据文章id取出文章作者共写了多少文章和相关文章
def getUserArticle(request, id):
    uu = models.article.objects.get(id=id).userinfo
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
        articles = models.article.objects.filter(**all_con).order_by('id').values(
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
    articles = models.article.objects.all().order_by('-like')[0:4]
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
    arts = models.article_collection.objects.filter(userinfo_id=list(userid)[0]['id']).values('article_id')
    arti = []
    res['article'] = arti
    for a in range(len(arts)):
        arttitle = \
            models.article.objects.filter(id=list(arts)[a]['article_id']).order_by('-id').values('id', 'title',
                                                                                                 'introduce',
                                                                                                 'upload',
                                                                                                 'userinfo__name',
                                                                                                 'like')[0]
        arti.append(arttitle)
    return JsonResponse(res)


# 删除收藏文章
def deleteArticle(request, id):
    try:
        delete_section = models.article_collection.objects.filter(article_id=id).delete()
        if delete_section[0]:
            return JsonResponse({"code": "888"})
        else:
            return JsonResponse({"code": "444"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 根据用户的tel获取用户写的文章
def getMyArticle(request, tel):
    res = {}
    userid = userdetail.objects.filter(telephone=tel).values('id')
    arts = models.article.objects.filter(userinfo_id=list(userid)[0]['id']).values('id')
    arti = []
    res['article'] = arti
    for a in range(len(arts)):
        arttitle = \
            models.article.objects.filter(id=list(arts)[a]['id']).order_by('-id').values('id', 'title', 'introduce',
                                                                                         'upload', 'like')[0]
        arti.append(arttitle)
    return JsonResponse(res)


# 删除个人文章
def deleteUserArticle(request, id):
    try:
        delete_section = models.article.objects.filter(id=id).delete()
        # print(delete_section)
        if delete_section[0]:
            return JsonResponse({"code": "888"})
        else:
            return JsonResponse({"code": "444"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 获取文章的所有评论（根据文章ID）
def getComment(request, artid, usertel):
    res = {}
    comments = models.comment.objects.order_by('-uptime').filter(article_id=artid)
    com_list = []
    for comm in comments:
        com_dict = model_to_dict(comm)
        del com_dict['article']
        # 是否点赞状态
        like_flag = False
        if usertel:
            uid = userdetail.objects.get(telephone=usertel).id
            res['user_id']=uid
            count = models.comment_like.objects.filter(comment_id=comm.id, user_id=uid).count()
            like_flag = count == 1 if True else False
        com_dict['like_flag'] = like_flag
        # 调用方法,通过用户id 获取用户name,iconurl，返回一个字典，封装到com_dict['user']
        com_dict['user'] = getUserByid(com_dict['user'])
        # 通过文章评论(comm),获取二级评论，返回一个列表，封装到com_dict['replys']
        com_dict['replys'] = getCommentByComId(comm, usertel)
        com_list.append(com_dict)
    # 当前文章id
    res['article_id'] = artid
    # 当前文章的一级评论、二级评论
    res['comments'] = com_list

    return JsonResponse(res)


# 通过评论ID(com_dict['id']),获取二级评论，返回一个列表
def getCommentByComId(comm, usertel):
    res = []
    # 当前评论的所有二级评论
    comments = comm.comment_comment_set.all()
    for com in comments:
        com_dict = model_to_dict(com)
        # 删除评论ID，数据冗余
        del com_dict['comment']
        # 是否点赞状态
        like_flag = False
        if usertel:
            uid = userdetail.objects.get(telephone=usertel).id
            count = models.comment_comment_like.objects.filter(comment_comment_id=com.id, user_id=uid).count()
            like_flag = count == 1 if True else False
        com_dict['like_flag'] = like_flag
        # 获得回帖人信息
        com_dict['user'] = getUserByid(com_dict['user'])
        res.append(com_dict)
    return res


# 调用方法,通过用户id 获取用户name,iconurl
def getUserByid(id):
    return userdetail.objects.filter(id=id).values('id', 'name', 'telephone', 'icon__iconurl')[0]


# 添加文章点赞
def insertArticleLike(request, articleid, tel):
    try:
        userid = userdetail.objects.get(telephone=tel).id
        articlelike = {
            "user_id": userid,
            "article_id": articleid
        }
        addart_like = models.article_like.objects.create(**articlelike)
        if addart_like:
            addart = models.article.objects.filter(id=articleid).update(like=F('like') + 1)
        return JsonResponse({"code": 999})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


#  删除文章点赞
def deteleArticleLike(request, articleid, tel):
    try:
        userid = userdetail.objects.get(telephone=tel).id
        addart_like = models.article_like.objects.filter(user_id=userid, article_id=articleid).delete()
        if addart_like:
            addart = models.article.objects.filter(id=articleid).update(like=F('like') - 1)
        return JsonResponse({"code": 999})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 评论点赞
def insertCommentLike(request, commid, tel):
    try:
        userid = userdetail.objects.get(telephone=tel).id
        com_like = models.comment_like.objects.filter(comment_id=commid, user_id=userid).count()
        if com_like:
            addart_like = models.comment_like.objects.filter(user_id=userid, comment_id=commid).delete()
            if addart_like:
                addart = models.comment.objects.filter(id=commid).update(like=F('like') - 1)
            return JsonResponse({"code": 999})
        else:
            commentlike = {
                "user_id": userid,
                "comment_id": commid
            }
            addart_like = models.comment_like.objects.create(**commentlike)
            if addart_like:
                addart = models.comment.objects.filter(id=commid).update(like=F('like') + 1)
            return JsonResponse({"code": 888})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 添加评论评论点赞
def insertReplyLike(request, replyid, tel):
    try:
        userid = userdetail.objects.get(telephone=tel).id
        rep_like = models.comment_comment_like.objects.filter(comment_comment_id=replyid, user_id=userid)
        if rep_like:
            addart_like = models.comment_comment_like.objects.filter(user_id=userid,
                                                                     comment_comment_id=replyid).delete()
            if addart_like:
                addart = models.comment_comment.objects.filter(id=replyid).update(like=F('like') - 1)
            return JsonResponse({"code": 999})
        else:
            replylike = {
                "user_id": userid,
                "comment_comment_id": replyid
            }
            addart_like = models.comment_comment_like.objects.create(**replylike)
            if addart_like:
                addart = models.comment_comment.objects.filter(id=replyid).update(like=F('like') + 1)
            return JsonResponse({"code": 999})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 添加文章评论内容
def insertArticleCommet(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            telephone = data['usertel']
            articleid = data['articleid']
            comment_article = data['comment_content']
            userid = userdetail.objects.get(telephone=telephone).id
            article_comment = {
                'content': comment_article,
                'uptime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'article_id': articleid,
                'user_id': userid
            }
            insertcomment = models.comment.objects.create(**article_comment)
            if insertcomment:
                return JsonResponse({"code": 888})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 添加评论回复内容
def insertCommentContent(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            telephone = data['usertel']
            commentid = data['commentid']
            comment_content = data['comment_content']
            userid = userdetail.objects.get(telephone=telephone).id
            comment = {
                'content': comment_content,
                'uptime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'comment_id': commentid,
                'user_id': userid
            }
            insertcomment = models.comment_comment.objects.create(**comment)
            if insertcomment:
                return JsonResponse({"code": 888})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})

# s删除文章评论
def deleteArticleComment(request,commid,articleid):
    try:
        a= models.comment_comment.objects.filter(comment_id=commid).count()
        if a:
            twocomment=models.comment_comment.objects.filter(comment_id=commid).values()
            two_comment=list(twocomment)
            if two_comment[0]['like']:
                comment_comment_like=models.comment_comment_like.objects.filter(comment_comment_id=two_comment[0]['id']).delete()
                deletetwocomment=models.comment_comment.objects.filter(id=two_comment[0]['id']).delete()
                comment_like=models.comment_like.objects.filter(comment_id=commid).delete()
            deletecomment=models.comment.objects.filter(id=commid).delete()
        else:
            comment=models.comment.objects.filter(id=commid).values()
            comment=list(comment)
            if comment[0]['like']:
                comment_like=models.comment_like.objects.filter(comment_id=commid).delete()
            deletecomment = models.comment.objects.filter(id=commid).delete()

        return JsonResponse({"code": 888})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})
# s删除评论回复
def deleteReply(request,comment_id):
    try:
        comment = models.comment_comment.objects.filter(id=comment_id).values('like')
        comment = list(comment)
        print(comment)
        if comment[0]['like'] >= 1:
            comment_like = models.comment_comment_like.objects.filter(
                comment_comment_id=comment_id).delete()
        comment = models.comment_comment.objects.filter(id=comment_id).delete()
        return JsonResponse({"code": 888})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})
