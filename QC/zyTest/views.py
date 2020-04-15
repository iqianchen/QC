from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
# import urllib.request

# from QC import config
from user import models
from user import serializers

import datetime


class JSONResponse(HttpResponse):
    """
        向http添加的内容
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



# 生成流水单号
def createTaskNo(num):
    today = datetime.date.today()
    strDate = today.strftime("%Y%m%d")
    orderNo = util(num)
    taskNo = 'ZYQC%s%s' % (strDate,orderNo)
    return taskNo
# 不足六位的补0
def util(autoNum):
    DEFAULT_LENGTH = 6
    strlen = len(str(autoNum))
    if (strlen > DEFAULT_LENGTH):
        return str(autoNum)
    while strlen < DEFAULT_LENGTH:  
        autoNum = '0%s' % (autoNum)
        strlen = strlen + 1
    return autoNum

num = 1
def addTest(request):
    # print(type(taskNo))
    global num
    num += 1
    taskNo = createTaskNo(num)
    return HttpResponse(taskNo)


