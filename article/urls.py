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
]
