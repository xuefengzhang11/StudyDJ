from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'course'

urlpatterns = [
    path('direction/', views.getDirection, name='direction'),  # 得到方向导航栏数据
    url(r'category/(?P<direid>\d+)', views.getCategory, name='category'),  # 得到方向导航栏数据(通过方向id查询)
    path('degree/', views.getDegree, name='degree'),  # 得到难度导航栏数据
    url(r'getCourses/(?P<direid>\d+),(?P<cateid>\d+),(?P<degrid>\d+),(?P<pindex>\d+)', views.getCourses,
        name='getCourses'),
    path('getHotCourse/', views.getHotCourse, name='getHotCourse'),  # 得到热门课程
    url(r'getCourse/(?P<id>\d*)', views.getCourseDetail, name='getCourseDetail'),  # 得到课程详情
    # ---

    #url(r'getCourseDetail/(?P<id>\d*)', views.getCourseDetail, name='getCourseDetail'),  # 得到课程详情

    # url(r'getCourse/dire/(?P<id>\d*)', views.getCourseByDirectionId, name='getCourseByDirectionId'),  # 根据课程方向ID得到视频
    # url(r'getCourse/degr/(?P<id>\d*)', views.getCourseByDegreeId, name='getCourseByDegreeId'),  # 根据课程难度ID得到视频

]
