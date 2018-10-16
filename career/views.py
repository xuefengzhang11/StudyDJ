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
def getCareer(request):
    careers_list = []
    careers = career.objects.order_by('-learn').all()
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


# -----

# 职业计划详情信息
def getCareerDetail(request, id):
    m_career = career.objects.filter(id=id).first()
    dict_career = model_to_dict(m_career)
    courses = []
    cours = m_career.course_set.all()
    # 每个课程小节数
    sects_num = 0
    # 每个课程章数
    chaps_num = 0
    for cour in cours:
        cour_dict = model_to_dict(cour)
        # 同理：将章封装到各自的节中
        chapters = []
        chaps = cour.chapter_set.all()
        chaps_num += len(list(chaps))
        for chap in chaps:
            chap_dict = model_to_dict(chap)
            # 同理：将节封装到各自的章中
            sections = []
            sects = cour.chapter_set.all()
            sects_num += len(list(sects))
            for sect in sects:
                sect_dict = model_to_dict(sect)
                # 将当前课程节追加到课程节列表中
                sections.append(sect_dict)
            # 将所有课程节封装到对应的课程章中

            chap_dict['sections'] = sections

            # 将当前课程章追加到课程章列表中
            chapters.append(chap_dict)

        # 将小节数加入到课程当中
        cour_dict['sects_num'] = sects_num
        # 将小节数加入到课程当中
        cour_dict['chaps_num'] = chaps_num
        # 将所有课程章封装到对应的课程中
        cour_dict['chapters'] = chapters
        # 将当前课程追加到课程列表中
        courses.append(cour_dict)
    # 将所有课程封装到职业计划中
    dict_career['courses'] = courses
    return JsonResponse({"career": dict_career}, json_dumps_params={'ensure_ascii': False})
