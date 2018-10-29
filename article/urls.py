from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'article'

urlpatterns = [
    # 得到热门文章
    path('hotArticle/', views.hotArticle, name='hotArticle'),
    # 根据ID得到文章信息
    url(r'getArticleById/(?P<id>\d+)/(?P<tel>\w*)/', views.getArticleById, name='getArticleById'),
    # 求文章总数
    url(r'^acountArticle\w*/(?P<con>\w*)/', views.acount, name='acount'),
    # 得到文章
    url(r'^getArticle/(?P<pageIndex>\d*)/(?P<con>\w*)/', views.getArticle, name='getArticle'),
    # 通过用户ID获取文章
    url(r'^getUserArticle/(?P<id>\d+)', views.getUserArticle, name='getUserArticle'),
    # 根据tel获取已经收藏的文章
    url(r'^getCollectArticle/(?P<tel>\d+)', views.getCollectArticle, name='getCollectArticle'),
    # 根据tel获取我的文章
    url(r'^getMyArticle/(?P<tel>\d+)', views.getMyArticle, name='getMyArticle'),
    # 通过文章ID获取文章所有评论
    url(r'getComment/(?P<artid>\d+)/(?P<usertel>\d*)', views.getComment, name='getComment'),
    # 删除收藏文章
    url(r'deleteArticle/(?P<id>\w*)', views.deleteArticle, name='deleteArticle'),
    # 删除个人文章
    url(r'deleteUserArticle/(?P<id>\w*)', views.deleteUserArticle, name='deleteUserArticle'),
    # 用户对文章点赞
    url(r'insertArticleLike/(?P<articleid>\w*)/(?P<tel>\d+)', views.insertArticleLike, name='insertArticleLike'),
    # 添加文章点赞
    url(r'deteleArticleLike/(?P<articleid>\w*)/(?P<tel>\d+)', views.deteleArticleLike, name='deteleArticleLike'),
    # 删除文章点赞
    url(r'insertCommentLike/(?P<commid>\w*)/(?P<tel>\d+)', views.insertCommentLike, name='insertCommentLike'),
    # 添加或者删除评论点赞
    url(r'insertReplyLike/(?P<replyid>\w*)/(?P<tel>\d+)', views.insertReplyLike, name='insertReplyLike'),
    # 添加或者删除评论评论点赞  # 添加文章评论内容
    url(r'insertArticleCommet/', views.insertArticleCommet, name='insertArticleCommet'),
    # 添加评论回复内容
    url(r'insertCommentContent/', views.insertCommentContent, name='insertCommentContent'),
    # 写文章
    url(r'commitArticle/(?P<tel>\d+)', views.commitArticle, name='commitArticle'),
    # 文章评论删除
    url(r'deleteArticleComment/(?P<commid>\w+)/(?P<articleid>\w+)', views.deleteArticleComment,
        name='deleteArticleComment'),
    # 删除回复删除
    url(r'deleteReply/(?P<comment_id>\w*)', views.deleteReply, name='deleteReply'),
]
