from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
# 导入模型
from career.models import career
import json

# 热门职业
def hotCareer(request):
    careers = career.objects.order_by('-learn').all()[0:4]
    careers_list=[]
    for care in careers:
        care_dict = model_to_dict(care)
        courses_list = getCourseByCareer(care)
        care_dict['courses'] = courses_list
        care_dict['coursesNum'] = len(courses_list)
        careers_list.append(care_dict)
    return JsonResponse(
            {"hotCareers": careers_list},json_dumps_params ={'ensure_ascii': False})

def getCareer(request, pageIndex):
    pageSize = 12
    pageIndex = int(pageIndex)
    start = (pageIndex - 1) * pageSize
    end = pageIndex * pageSize
    careers_list = []
    careers = career.objects.order_by('-learn').all()[start:end]
    for care in careers:
        care_dict = model_to_dict(care)
        courses_list = getCourseByCareer(care)
        care_dict['courses'] = courses_list
        care_dict['coursesNum'] = len(courses_list)
        careers_list.append(care_dict)
    return JsonResponse({"careers": careers_list}, json_dumps_params={'ensure_ascii': False})

# 通过职业计划获取所有课程
def getCourseByCareer(care):
    courses = care.course_set.all()
    courses_list = []
    for cour in courses:
        cour_dict = model_to_dict(cour)
        chapters_list = getChapterByCourse(cour)
        cour_dict['chapters'] = chapters_list
        cour_dict['chaptersNum'] = len(chapters_list)
        courses_list.append(cour_dict)
    return courses_list
# 通过课程获取所有章
def getChapterByCourse(cour):
    chapters = cour.chapter_set.all()
    chapters_list = []
    for chap in chapters:
        chap_dict = model_to_dict(chap)
        sections_list = getSectionByChapter(chap)
        chap_dict['sections'] = sections_list
        chap_dict['sectionsNum'] = len(sections_list)
        chapters_list.append(chap_dict)
    return chapters_list
# 通过所有章获取所有节
def getSectionByChapter(chap):
    sections = chap.section_set.all()
    sections_list = []
    for sect in sections:
        sections_list.append(model_to_dict(sect))
    return sections_list

# 通过职业id获取详细课程
def getCareerDetail(request,careerid):
    careers = career.objects.get(id=careerid)
    careers=model_to_dict(careers)
    care = career.objects.get(id=careerid)
    course_all={}
    courses_list = getCourseByCareer(care)
    course_all['courses'] = courses_list
    course_all['careers'] = careers
    return JsonResponse({"careers": course_all}, json_dumps_params={'ensure_ascii': False})

# ----
# 返回职业的数量
def getCount(request):
    try:
        len = career.objects.all().count()
        return JsonResponse({'account':len})
    except Exception as ex:
        return JsonResponse({"code":"409"})
