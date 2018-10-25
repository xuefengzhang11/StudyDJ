from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'course'

urlpatterns = [
    # 得到方向导航栏数据
    path('direction/', views.getDirection, name='direction'),
    # 得到方向导航栏数据(通过方向id查询)
    url(r'category/(?P<direid>\d+)', views.getCategory, name='category'),
    # 得到难度导航栏数据
    path('degree/', views.getDegree, name='degree'),
    # 多条件查询课程
    url(r'getCourses/(?P<direid>\d+),(?P<cateid>\d+),(?P<degrid>\d+),(?P<con>\w*),(?P<pindex>\d+)', views.getCourses,
        name='getCourses'),
    # 多条件查询课程数量
    url(r'getCoursesCount/(?P<direid>\d+),(?P<cateid>\d+),(?P<degrid>\d+),(?P<con>\w*)', views.getCoursesCount,
        name='getCoursesCount'),
    # 得到热门课程
    path('getHotCourse/', views.getHotCourse, name='getHotCourse'),
    # 得到课程详情
    url(r'getCourse/(?P<id>\d*)', views.getCourseDetail, name='getCourseDetail'),

    # 个人中心最近学习
    url(r'getFreeCoursePersonal/(?P<tel>\w*)', views.getFreeCoursePersonal, name='getFreeCoursePersonal'),  # 个人中心页最近学习
    url(r'deleteFreeCoursePersonal/(?P<courid>\w*)', views.deleteFreeCoursePersonal, name='deleteFreeCoursePersonal'),
    # 个人中心页课程删除
    url(r'getCollectCoursePersonal/(?P<tel>\w*)', views.getCollectCoursePersonal, name='getCollectCoursePersonal'),
    # 个人中心页课程收藏
    url(r'deleteCollectCoursePersonal/(?P<courid>\w*)', views.deleteCollectCoursePersonal,
        name='deleteCollectCoursePersonal'),  # 个人中心页

    # 课程详情页收藏课程
    url(r'insertCollectCourse/(?P<course_id>\w*)/(?P<tel>\w*)', views.insertCollectCourse, name='collectcourse'),
    # 收藏课程
    url(r'collectJudge/(?P<course_id>\w*)/(?P<tel>\w*)', views.collectJudge, name='collectJudge'),  # 判断收藏课程
    url(r'deteleCollectCourse/(?P<course_id>\w*)/(?P<tel>\w*)', views.deteleCollectCourse, name='deteleCollectCourse'),
    # 删除课程

    # 视频页
    url(r'getSectiondata/(?P<sectid>\w*)/(?P<careerid>\w*)', views.getSectiondata, name='getSectiondata'),

    # 课程节获取所有评论，一级评论、二级评论
    url(r'getComment/(?P<sectid>\d+)/(?P<usertel>\d*)', views.getComment, name='getComment'),  # 通过文章ID获取文章所有评论

    # 添加课程到最近学习
    url(r'addSectionHistory/(?P<sectid>\d+)/(?P<usertel>\d*)', views.addSectionHistory, name='addSectionHistory'),

    # 添加或者删除评论点赞
    url(r'insertCommentLike/(?P<commid>\w*)/(?P<tel>\d+)', views.insertCommentLike, name='insertCommentLike'),

    # 添加或者删除评论评论点赞
    url(r'insertReplyLike/(?P<replyid>\w*)/(?P<tel>\d+)', views.insertReplyLike, name='insertReplyLike'),
     # 添加文章评论内容
    url(r'insertSectionCommet/', views.insertSectionCommet, name='insertSectionCommet'),
    # 添加评论回复内容
    url(r'insertCommentContent/', views.insertCommentContent, name='insertCommentContent'),
    # 视频评论删除
    url(r'deleteSectionComment/(?P<sectid>\w*)/(?P<commid>\w+)', views.deleteSectionComment, name='deleteSectionComment'),
    # 删除回复删除
    url(r'deleteReply/(?P<comment_id>\w*)', views.deleteReply, name='deleteReply'),
    # 根据用户电话查到导航揽人物用到的信息
    url(r'getNextData/(?P<usertel>\w*)', views.getNextData, name='getNextData'),


]
