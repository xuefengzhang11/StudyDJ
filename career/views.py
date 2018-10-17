from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
# 导入模型
from career.models import career
import json


def hotCareer(request):
    careers = career.objects.order_by('-learn').all()[0:4]
    careers_temp = career.objects.order_by('-learn').all()[0:4].values()
    # 统计有多少课程
    course_count = []
    # 统计有多少个章
    chapter_count = []
    # 统计有多少个小节
    section_count = []
    for care in careers:
        # 通过career_id 找到所有课程
        courses = care.course_set.all()
        # 课程数
        course_count.append({care.id: len(list(courses))})
        # 这里开始找章数
        chap_num = 0
        sect_num = 0
        for cour in courses:
            chapters = cour.chapter_set.all()
            # 课程章数
            chap_num += len(list(chapters))
            # 这里开始找小节数
            for chap in chapters:
                sections = chap.section_set.all()
                sect_num += len(list(sections))
        section_count.append({care.id: sect_num})
        chapter_count.append({care.id: chap_num})
    return JsonResponse(
        {"hotCareers": list(careers_temp), "course_count": course_count, "chapter_count": chapter_count,
         "section_count": section_count},
        json_dumps_params={'ensure_ascii': False})

# 获取所有职业计划
def getCareer(request, pageIndex):
    pageSize = 8
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
    care = career.objects.get(id=careerid)
    course_all={}
    courses_list = getCourseByCareer(care)
    course_all['courses'] = courses_list
    return JsonResponse({"careers": course_all}, json_dumps_params={'ensure_ascii': False})





# ----
# 返回职业的数量
def getCount(request):
    try:
        len = career.objects.all().count()
        print(len)
        return JsonResponse({'account':len})
    except Exception as ex:
        return JsonResponse({"code":"409"})
