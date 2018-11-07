from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'career'

urlpatterns = [
    # 得到热门职业
    path('hotCareer/', views.hotCareer, name='hotCareer'),
    # 得到职业总数
    path('getcount/', views.getCount, name='getCount'),
    # 得到职业详情页
    url(r'getcareerdetail/(?P<careerid>\d*)/', views.getCareerDetail, name='getCareerDetail'),
    # 得到所有职业
    # url(r'^getcareer/(?P<pageIndex>\d*)/', views.getCareer, name='getCareer'),
    # 用完删
    url(r'^getcareer/(?P<pageIndex>\d*)/', views.temp, name='getCareer'),

]
