from django.http import HttpResponse, JsonResponse
import json
from django.forms.models import model_to_dict

# from . import models
# 导入模型
from course.models import course, direction, category, degree


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


# 按条件查询课程
def getCourses(request, direid, cateid, degrid, pindex):
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
    pageSize = 4
    start = pageSize * (pindex - 1)
    end = pageSize * pindex
    # 未选择课程难度
    if degrid == 0:
        # 未选择分类
        if cateid == 0:
            # 未选择方向
            if direid == 0:
                courses = course.objects.all().values(
                    'id', 'name', 'imgurl', 'introduce', 'cs_degree__name', 'learn')[start:end]
            # 选择了方向
            else:
                courses = course.objects.filter(cs_direction_id=direid).values(
                    'id', 'name', 'imgurl', 'introduce', 'cs_degree__name', 'learn')[start:end]
        # 选择了分类（自动选择方向）
        else:
            courses = course.objects.filter(cs_direction_id=direid, cs_category_id=cateid).values(
                'id', 'name', 'imgurl', 'introduce', 'cs_degree__name', 'learn')[start:end]
    # 选择了课程难度
    else:
        # 未选择分类
        if cateid == 0:
            # 未选择方向
            if direid == 0:
                courses = course.objects.filter(cs_degree_id=degrid).values(
                    'id', 'name', 'imgurl', 'introduce', 'cs_degree__name', 'learn')[start:end]
            # 选择了方向
            else:
                courses = course.objects.filter(cs_direction_id=direid, cs_degree_id=degrid).values(
                    'id', 'name', 'imgurl', 'introduce', 'cs_degree__name', 'learn')[start:end]
        # 选择了分类（自动选择方向）
        else:
            courses = course.objects.filter(
                cs_direction_id=direid, cs_category_id=cateid, cs_degree_id=degrid).values(
                'id', 'name', 'imgurl', 'introduce', 'cs_degree__name', 'learn')[start:end]
    print(courses)
    return JsonResponse({"courses": list(courses)}, json_dumps_params={'ensure_ascii': False})


# 得到热门课程
def getHotCourse(request):
    hotCourses = course.objects.order_by('-learn').all().values(
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


'''
# 将模型对象转化为字典
    cour_dict = model_to_dict(cour)
    # 课程难度
    cour_dict['degree'] = cour.cs_degree.name
    # 课程方向
    cour_dict['direction'] = cour.cs_direction.name
    # 课程分类
    cour_dict['category'] = cour.cs_category.name
    # 得到所有的章
    chaps = cour.chapter_set.all()
    chapters = []
    for chap in chaps:
        chap_dict = model_to_dict(chap)
        # 得到所有的小节
        sects = chap.section_set.all().values()
        chap_dict['sections'] = list(sects)
        chapters.append(chap_dict)
    # hotcourses = getHotCourse()
'''
