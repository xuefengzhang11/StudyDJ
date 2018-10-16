from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
import json


# 思达迪首页
def home(request):
    user = {
        "id": "001",
        "name": "hyy"
    }
    return HttpResponse(json.dumps(user))
    # return render(request,'study_index.html')
