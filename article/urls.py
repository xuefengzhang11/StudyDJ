from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'article'

urlpatterns = [

    path('hotArticle/', views.hotArticle, name='hotArticle'),  # 得到热门文章
    url(r'getArticle/(?P<id>\d+)', views.getArticle, name='getArticle'),  # 根据ID得到文章信息
]
