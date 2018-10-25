from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.db import connection
from datetime import datetime
# ---导入与自定义模块
from user.models import user, userdetail
from . import models
from utils.utils import dictfetchall
from course.models import course, direction, category, degree
from django.db.models import F
import json

# 课程方向
def getDirection(request):
    directions = direction.objects.all().values()
    return JsonResponse({"directions": list(directions)}, json_dumps_params={'ensure_ascii': False})


# 课程分类(通过方向ID)
def getCategory(request, direid):
    direid = int(direid)
    if direid == 0:
        categorys = category.objects.all().values()
    else:
        categorys = category.objects.filter(ctgr_direction_id=direid).values()
    return JsonResponse({"categorys": list(categorys)}, json_dumps_params={'ensure_ascii': False})


# 课程难度
def getDegree(request):
    degrees = degree.objects.all().values()
    return JsonResponse({"degrees": list(degrees)}, json_dumps_params={'ensure_ascii': False})


# 按条件查询课程（多条件筛选）
def getCourses(request, direid, cateid, degrid, con, pindex):
    '''
    :param direid: 课程方向ID
    :param cateid: 课程分类ID
    :param degrid: 课程难度ID
    :param pindex: 查询的课程页码
    :return: 返回符合要求的所有课程信息
    '''
    direid = int(direid)
    cateid = int(cateid)
    degrid = int(degrid)
    pindex = int(pindex)
    pageSize = 12
    start = pageSize * (pindex - 1)
    end = pageSize * pindex
    all_con = {}
    if direid:
        all_con['cs_direction_id'] = direid
    if cateid:
        all_con['cs_category_id'] = cateid
    if degrid:
        all_con['cs_degree_id'] = degrid
    if con:
        all_con['name__icontains'] = con
    courses = course.objects.filter(**all_con).order_by('id').values(
        'id', 'name', 'imgurl', 'introduce', 'cs_degree__name', 'learn')[start:end]
    return JsonResponse({"courses": list(courses)}, json_dumps_params={'ensure_ascii': False})


# 按条件查询课程总数量
def getCoursesCount(request, direid, cateid, degrid, con):
    '''
    :param direid: 课程方向ID
    :param cateid: 课程分类ID
    :param degrid: 课程难度ID
    :return: 返回符合要求的所有课程信息
    '''
    direid = int(direid)
    cateid = int(cateid)
    degrid = int(degrid)
    all_con = {}
    if direid:
        all_con['cs_direction_id'] = direid
    if cateid:
        all_con['cs_category_id'] = cateid
    if degrid:
        all_con['cs_degree_id'] = degrid
    if con:
        all_con['name__icontains'] = con
    alls = course.objects.filter(**all_con).count()
    return JsonResponse({"alllength": alls}, json_dumps_params={'ensure_ascii': False})


# 得到热门课程
def getHotCourse(request):
    hotCourses = course.objects.order_by('?').all().values(
        'id', 'name', 'imgurl', 'introduce', 'cs_degree__name', 'learn')[0:4]
    return JsonResponse({"hotCourses": list(hotCourses)}, json_dumps_params={'ensure_ascii': False})


# 得到详细课程信息(id,课程名,课程方向,课程分类,课程难度 课程章 课程节)
def getCourseDetail(request, id):
    # 查询课程
    cour = course.objects.filter(id=id).values(
        'id', 'name', 'introduce', 'cs_direction__id', 'cs_direction__name', 'cs_category__id', 'cs_category__name'
        , 'cs_degree__id', 'cs_degree__name', 'learn')[0]
    chapters = getChaptersByCourse(course.objects.get(id=id))
    cour['chapters'] = chapters
    return JsonResponse(cour, json_dumps_params={'ensure_ascii': False})


# 通过课程查询章(返回一个字典列表)
def getChaptersByCourse(cour):
    chaps = cour.chapter_set.all()
    chapters_list = []
    for chap in chaps:
        sections = getSectionsByChapter(chap)
        chap_dict = model_to_dict(chap)
        chap_dict['sections'] = sections
        chapters_list.append(chap_dict)
    return chapters_list


# 通过章查询节(返回一个字典列表)
def getSectionsByChapter(chap):
    sects = chap.section_set.all()
    sections_list = []
    for sect in sects:
        sections_list.append(model_to_dict(sect))
    return sections_list


# --------------------


# 热门课程
def hotCourse(request):
    courses = getHotCourse()
    return JsonResponse({"hotCourses": list(courses)}, json_dumps_params={'ensure_ascii': False})


# 个人中心页（获取免费课程）
# 最近学习
def getFreeCoursePersonal(request, tel):
    try:
        cursor = connection.cursor()  # cursor = connections['default'].cursor()
        cursor.execute("""select cs.id as section_id,cs.name as section_name,ch.watchtime as history_watchtime,ccou.name as course_name,ccou.id as courid,
ccou.learn as course_learn,ccou.imgurl as cour_imgurl from user_user as u INNER JOIN course_history as ch INNER JOIN course_section as cs 
INNER JOIN course_chapter as cc INNER JOIN course_course as ccou
on u.id = ch.user_id and ch.section_id = cs.id and cs.chapter_id=cc.id and cc.course_id=ccou.id
where u.telephone=%s ORDER BY ch.watchtime desc""", [tel])
        row = dictfetchall(cursor)
        print(row)
        section_id = row[0]["section_id"]
        return JsonResponse({"nextstudy": row})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 个人中心最近学习删除节
def deleteFreeCoursePersonal(request, courid):
    print(courid)
    try:
        delete_section = models.history.objects.filter(section_id=courid).delete()
        # print(delete_section)
        if delete_section[0]:
            return JsonResponse({"code": "888"})
        else:
            return JsonResponse({"code": "444"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 个人中心课程收藏页
def getCollectCoursePersonal(request, tel):
    try:
        cursor = connection.cursor()  # cursor = connections['default'].cursor()
        cursor.execute("""select ccou.id as course_id ,ccou.imgurl as cour_imgurl,ccou.name as course_name,ccou.price as course_price,cco.collecttime as course_collecttime 
from user_user as u INNER JOIN course_collection as cco INNER JOIN  course_course as ccou
on u.id = cco.user_id and cco.course_id = ccou.id 
where u.telephone=%s
ORDER BY cco.collecttime""", [tel])
        row = dictfetchall(cursor)
        for ro in row:
            course_id = ro['course_id']
            cursor.execute("""select count(course_id) as coursenum from course_collection where course_id=%s""",
                           [course_id])
            coursenum = dictfetchall(cursor)
            ro['coursenum'] = coursenum[0]['coursenum']
        return JsonResponse({"collectcourse": row})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 个人中心课程收藏删除节
def deleteCollectCoursePersonal(request, courid):
    try:
        delete_course = models.collection.objects.filter(course_id=courid).delete()
        if delete_course[0]:
            return JsonResponse({"code": "888"})
        else:
            return JsonResponse({"code": "444"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 课程详情页收藏课程
def insertCollectCourse(request, course_id, tel):
    try:
        userid=user.objects.filter(telephone=tel).values('id')
        user_id=list(userid)[0]['id']  #得到用户的id
        collect = {
            "collecttime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "course_id": course_id,
            "user_id": user_id
        }
        res = models.collection.objects.create(**collect)
        return JsonResponse({"code": 888})  # 收藏成功
        userid = user.objects.filter(telephone=tel).values('id')
        user_id = list(userid)[0]['id']  # 得到用户的id
        havecollect = models.collection.objects.filter(course_id=course_id).values()  # 判断数据库里是否收藏
        if havecollect:
            return JsonResponse({"code": 444})
        else:
            collect = {
                "collecttime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "course_id": course_id,
                "user_id": user_id
            }
            res = models.collection.objects.create(**collect)
            return JsonResponse({"code": 888})  # 收藏成功
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 判断是否收藏
def collectJudge(request, course_id, tel):
    try:
        userid = user.objects.filter(telephone=tel).values('id')
        user_id = list(userid)[0]['id']  # 得到用户的id
        iscollect = models.collection.objects.filter(course_id=course_id, user_id=user_id).values()  # 判断是否收藏过
        if iscollect:
            return JsonResponse({"code": 888})  # 收藏状态
        else:
            return JsonResponse({"code": 444})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# s删除收藏课程
def deteleCollectCourse(request, course_id, tel):
    try:
        userid = user.objects.filter(telephone=tel).values('id')
        user_id = list(userid)[0]['id']  # 得到用户的id
        res = models.collection.objects.filter(course_id=course_id, user_id=user_id).values()
        affected_rows = models.collection.objects.filter(course_id=course_id, user_id=user_id).delete()

        if affected_rows:
            return JsonResponse({"code": "888"})  #删除成功
        else:
            return JsonResponse({"code": "444"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 视频页得到数据
def getSectiondata(request, sectid, careerid):
    try:
        sections = []
        cours = []
        all = {}
        section_data = models.section.objects.filter(id=sectid).values()
        sectiondata = list(section_data)
        # print(sectiondata[0])
        collectcourse = models.collection.objects.filter(course_id=careerid).count()
        course_data = models.course.objects.filter(id=careerid).values()
        coursedata = list(course_data)
        cours.append(coursedata)
        # print(coursedata)
        sectiondata[0]['coursenum'] = collectcourse
        sectiondata[0]['coursedata'] = cours[0]
        # print(sectiondata)
        return JsonResponse({'data': sectiondata})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})


# 课程节评论部分
def getComment(request, sectid, usertel):
    res = {}
    # 当前课程节id
    res['section_id'] = sectid
    comments = models.sectioncomment.objects.order_by('-uptime').filter(section_id=sectid)
    com_list = []
    for comm in comments:
        com_dict = model_to_dict(comm)
        like_flag = False
        if usertel:
            uid = userdetail.objects.get(telephone=usertel).id
            count = models.sectioncomment_like.objects.filter(user_id=uid, sectioncomment_id=comm.id).count()
            like_flag = count == 1 if True else False
            res['user_id'] = uid
        com_dict['like_flag'] = like_flag
        # 通过用户id获取用户name, iconurl，返回一个字典，封装到com_dict['user']
        com_dict['user'] = userdetail.objects.filter(id=com_dict['user']).values('id', 'name', 'icon__iconurl')[0]
        # 通过课程节评论(comm),获取二级评论，返回一个列表，封装到com_dict['replys']
        com_dict['replys'] = getCommentByComm(comm, usertel)
        com_list.append(com_dict)
    # 当前课程节的一级评论、二级评论
    res['comments'] = com_list
    return JsonResponse(res)


# 通过一个评论获取二级评论
def getCommentByComm(comm, usertel):
    res = []
    # 当前评论的所有二级评论
    comments = comm.sectioncomment_comment_set.all()
    for com in comments:
        com_dict = model_to_dict(com)
        like_flag = False
        if usertel:
            uid = userdetail.objects.get(telephone=usertel).id
            count = models.sectioncomment_comment_like.objects.filter(sectioncomment_comment_id=com.id,
                                                                      user_id=uid).count()
            like_flag = count == 1 if True else False
            print(com_dict['id'])
        com_dict['like_flag'] = like_flag
        # 获得恢复评论的用户信息
        com_dict['user'] = userdetail.objects.filter(id=com_dict['user']).values('id', 'name', 'icon__iconurl')[0]
        res.append(com_dict)
    return res


# 添加课程到最近学习
def addSectionHistory(request, sectid, usertel):
    try:
        # 先判断有没有添加过最近学习，有就修改，没有就添加
        # 通过用户电话号码获取用户id
        uid = user.objects.get(telephone=usertel).id
        count = models.history.objects.filter(user_id=uid, section_id=sectid).count()
        if count:
            # 修改 (删除->添加)
            models.history.objects.filter(user_id=uid, section_id=sectid).delete()
        models.history.objects.create(user_id=uid, section_id=sectid)
    except Exception as e:
        print(e)
        return JsonResponse({"res": "失败"})
    return JsonResponse({"res": "成功"})



# 评论点赞
def insertCommentLike(request,commid,tel):
    try:
        userid=userdetail.objects.get(telephone=tel).id
        com_like = models.sectioncomment_like.objects.filter(sectioncomment_id=commid, user_id=userid).count()
        if com_like:
            addart_like = models.sectioncomment_like.objects.filter(user_id=userid, sectioncomment_id=commid).delete()
            if addart_like:
                addart = models.sectioncomment.objects.filter(id=commid).update(like=F('like') - 1)
            return JsonResponse({"code": 999})
        else:
            commentlike={
                "user_id":userid,
                "sectioncomment_id":commid
            }
            addart_like=models.sectioncomment_like.objects.create(**commentlike)
            if addart_like:
                addart=models.sectioncomment.objects.filter(id=commid).update(like=F('like')+1)
            return JsonResponse({"code":888})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code":404})

# 添加评论评论点赞
def insertReplyLike(request,replyid,tel):
    try:
        userid=userdetail.objects.get(telephone=tel).id
        rep_like=models.sectioncomment_comment_like.objects.filter(sectioncomment_comment_id=replyid,user_id=userid)
        if rep_like:
            addart_like = models.sectioncomment_comment_like.objects.filter(user_id=userid,sectioncomment_comment_id=replyid).delete()
            if addart_like:
                addart = models.sectioncomment_comment.objects.filter(id=replyid).update(like=F('like') - 1)
            return JsonResponse({"code": 999})
        else:
            replylike={
                "user_id":userid,
                "sectioncomment_comment_id":replyid
            }
            addart_like=models.sectioncomment_comment_like.objects.create(**replylike)
            if addart_like:
                addart=models.sectioncomment_comment.objects.filter(id=replyid).update(like=F('like')+1)
            return JsonResponse({"code":999})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code":404})

# 添加视频评论内容
def insertSectionCommet(request):
    try:
        if request.method == 'POST':
            data = request.POST
            telephone = data['usertel']
            sectionid = data['sectionid']
            comment_section = data['comment_content']
            userid = userdetail.objects.get(telephone=telephone).id
            section_comment = {
                'content': comment_section,
                'uptime':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'section_id':sectionid,
                'user_id':userid
            }
            insertcomment=models.sectioncomment.objects.create(**section_comment)
            if insertcomment:
                return JsonResponse({"code":888})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code":404})

# 添加评论回复内容
def insertCommentContent(request):
    try:
        if request.method == 'POST':
            data=request.POST
            # print(type(request.body.decode()))
            # data = json.loads(request.body.decode())
            # data = json.loads(request.body.decode('utf-8'))
            telephone = data['usertel']
            commentid = data['commentid']
            comment_content = data['comment_content']
            userid = userdetail.objects.get(telephone=telephone).id
            comment = {
                'content': comment_content,
                'uptime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'sectioncomment_id': commentid,
                'user_id': userid
            }
            insertcomment = models.sectioncomment_comment.objects.create(**comment)
            if insertcomment:
                return JsonResponse({"code": 888})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})

# s删除视频评论
def deleteSectionComment(request,sectid,commid):
    try:
        a=models.sectioncomment_comment.objects.filter(sectioncomment_id=commid).count()
        if a:
            twocomment=models.sectioncomment_comment.objects.filter(sectioncomment_id=commid).values()
            twocomment=list(twocomment)
            if twocomment[0]['like']:
                comment_comment_like=models.sectioncomment_comment_like.objects.filter(sectioncomment_comment_id=twocomment[0]['id']).delete()
                comment_comment=models.sectioncomment_comment.objects.filter(id=twocomment[0]['id']).delete()
                comment_like=models.sectioncomment.objects.filter(id=commid).values()
                comment_like=list(comment_like)
                if comment_like[0]['like']>=1:
                    comment_likes=models.sectioncomment_like.objects.filter(sectioncomment_id=commid).delete()
                comment=models.sectioncomment.objects.filter(id=commid).delete()
            else:
                deletetwo=models.sectioncomment_comment.objects.filter(id=twocomment[0]['id']).delete()
                comment_like=models.sectioncomment.objects.filter(id=commid).values()
                comment_like=list(comment_like)
                if comment_like[0]['like']>=1:
                    comment_likes=models.sectioncomment_like.objects.filter(sectioncomment_id=commid).delete()
                deletecomment=models.sectioncomment.objects.filter(id=commid).delete()
        else:
            comment=models.sectioncomment.objects.filter(id=commid).values()
            comment=list(comment)
            if comment[0]['like']:
                comment_like=models.sectioncomment_like.objects.filter(sectioncomment_id=commid).delete()
            comment=models.sectioncomment.objects.filter(id=commid).delete()
        return JsonResponse({"code":888})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})

# s删除评论回复
def deleteReply(request,comment_id):
    try:
        comment=models.sectioncomment_comment.objects.filter(id=comment_id).values('like')
        comment=list(comment)
        print(comment)
        if comment[0]['like']>=1:
            comment_like = models.sectioncomment_comment_like.objects.filter(sectioncomment_comment_id=comment_id).delete()
        comment = models.sectioncomment_comment.objects.filter(id=comment_id).delete()
        return JsonResponse({"code":888})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code": 404})

 # 根据用户电话查到导航揽人物用到的信息
def getNextData(request,usertel):
    userid=userdetail.objects.get(telephone=usertel).id
    sectid=models.history.objects.order_by('-watchtime').filter(user_id=userid).values('id')
    sectid1=sectid[0]['id']
    res=IndexSectionId(sectid1)
    res['sectid']=sectid1
    return JsonResponse({"data":res})
def IndexSectionId(sectid):
    res = {}
    sec_chapterid = models.section.objects.get(id=sectid).chapter_id
    chap_secs = models.section.objects.filter(chapter_id=sec_chapterid).values('id','name')
    for cs in range(len(list(chap_secs))):
        if int(sectid) == list(chap_secs)[cs]['id']:
            section_index = cs + 1
            res['section_index'] = section_index
            res['section_name'] = list(chap_secs)[cs]['name']

    chap_courseid = models.chapter.objects.get(id=sec_chapterid).course_id
    cour_chaps = models.chapter.objects.filter(course_id=chap_courseid).values('id','course__name')
    for cc in range(len(list(cour_chaps))):
        if int(sec_chapterid) == list(cour_chaps)[cc]['id']:
            chapter_index = cc + 1
            res['chapter_index'] = chapter_index
            res['course_name'] = list(cour_chaps)[cc]['course__name']
    return res

