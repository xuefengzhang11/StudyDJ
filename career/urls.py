from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'career'

urlpatterns = [


    path('hotCareer/', views.hotCareer, name='hotCareer'),  # 得到热门职业
    path('getCareer/', views.getCareer, name='getCareer'),  # 得到所有职业
    url(r'getCareerDetail/(?P<id>\d*)', views.getCareerDetail, name='getCareerDetail'),  # 得到职业计划详情

]
