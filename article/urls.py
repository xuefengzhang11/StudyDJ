from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'article'

urlpatterns = [
    path('hotArticle/', views.hotArticle, name='hotArticle'),  # 得到热门文章
    url(r'getArticleById/(?P<id>\d+)', views.getArticleById, name='getArticleById'),  # 根据ID得到文章信息

    url(r'^acountArticle\w*/(?P<con>\w*)/', views.acount, name='acount'),  # 求文章总数
    url(r'^getArticle/(?P<pageIndex>\d*)/(?P<con>\w*)/', views.getArticle, name='getArticle'),  # 得到文章
    url(r'^getUserArticle/(?P<id>\d+)', views.getUserArticle, name='getUserArticle'),
    url(r'^getCollectArticle/(?P<tel>\d+)', views.getCollectArticle, name='getCollectArticle'),  # 根据tel获取已经收藏的文章
    url(r'^getMyArticle/(?P<tel>\d+)', views.getMyArticle, name='getMyArticle'),  # 根据tel获取我的文章
    url(r'deleteArticle/(?P<id>\w*)', views.deleteArticle, name='deleteArticle'),  # 个人中心页删除我的文章

    url(r'getComment/(?P<artid>\d+)', views.getComment, name='getComment') # 通过文章ID获取文章所有评论

]
