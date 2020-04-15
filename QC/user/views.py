from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import urllib.request


# import time
# import hashlib
# import urllib
from . import sign

from QC import config
from . import models
from . import serializers


AppInfo = config.AppInfo()
class JSONResponse(HttpResponse):
    """
        向http添加的内容
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# 判断用户是否存在
def isUser(userId):
    try:
        user = models.UserInfo.objects.get(userId=userId)
    except user.DoesNotExist:
        return HttpResponse('user does not exist',status=404)
    return user


# 接口      ------------------------------------------

# 验证
def getJSAPI(request):
    # return HttpResponse('1111')
    url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (
    AppInfo.AppKey, AppInfo.AppSecret)
    res_data = urllib.request.urlopen(url)
    
    res = JSONParser().parse(res_data)
    print('res_data1',res)
    access_token = res['access_token']
    print('access_token',access_token)

    url = 'https://oapi.dingtalk.com/get_jsapi_ticket?access_token=%s' % (access_token)
    res_data = urllib.request.urlopen(url)
    
    res = JSONParser().parse(res_data)
    print('res_data2',res)
    ticket = res['ticket']
    print('ticket',ticket)
    sign1 = sign.Sign(ticket,'http://sofa-geek.cn:9094')
    print('sign1',sign1)
    # print('sign',sign1.sign())
    newData = {
        'data': sign1.sign()
    }
    
    return JSONResponse(newData)


# 获取当前用户的详细信息
def getUserInfo(request, code):
    if request.method == 'GET':
        url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (
            AppInfo.AppKey, AppInfo.AppSecret)
        res_data = urllib.request.urlopen(url)
        res = JSONParser().parse(res_data)
        access_token = res['access_token']

        url = 'https://oapi.dingtalk.com/user/getuserinfo?access_token=%s&code=%s' % (
            access_token, code)
        res_data = urllib.request.urlopen(url)
        res = JSONParser().parse(res_data)
        userId = res['userid']

        url = 'https://oapi.dingtalk.com/user/get?access_token=%s&userid=%s' % (
            access_token, userId)
        res_data = urllib.request.urlopen(url)
        return HttpResponse(res_data, status=200)
    return JSONResponse('page not found', status=404)


# 添加用户
@csrf_exempt
def addUser(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        userType = request.POST.get('type')
        createUser = request.POST.get('createUser')
        if (userId == None or userType == None or createUser == None):
             return JSONResponse('Parameter error!',status=400)

        url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (
            AppInfo.AppKey, AppInfo.AppSecret)
        res_data = urllib.request.urlopen(url)
        res = JSONParser().parse(res_data)
        access_token = res['access_token']

        url = 'https://oapi.dingtalk.com/user/get?access_token=%s&userid=%s' % (
            access_token, userId)
        res_data = urllib.request.urlopen(url)
        res = JSONParser().parse(res_data)
        print('res',res)
        if ('errcode' in res and res['errcode'] == 60121):
            return JSONResponse('The user could not be found', status=404)
        add_data = {
            'userId': res['userid'],
            'name': res['name'],
            'type': userType,
            'position': res['position'] if 'position' in res else '',
            'avatar': res['avatar'],
            'jobNumber': res['jobNumber'] if 'jobNumber' in res else '',
            'openId': res['openId'],
            'createUser': createUser
        }

        serializer = serializers.UserInfoSerializer(data=add_data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse('true', status=200)
        else:
            print(serializer.errors)
            return JSONResponse('User already exists and cannot be added repeatedly', status=400)
    return JSONResponse('page not found', status=404)


# 查询用户
# 根据用户类型返回对应的用户数组
@csrf_exempt
def get(request):
    if request.method == 'POST':
        userType = request.POST.get('type')
        try:
            users = models.UserInfo.objects.filter(type=userType)
        except models.UserInfo.DoesNotExist:
            return HttpResponse('user does not exist',status=404)
        serializer = serializers.UserInfoSerializer(users, many=True)
        return JSONResponse(serializer.data)
    return JSONResponse('page not found', status=404)


# 修改用户
@csrf_exempt
def update(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        avatar = request.POST.get('avatar')
        jobNumber = request.POST.get('jobNumber')
        updateUser = request.POST.get('updateUser')
        if (userId == None or avatar == None or jobNumber == None or updateUser == None):
            return JSONResponse('Parameter error', status=400)

        user = isUser(userId)
        user.avatar = avatar
        user.jobNumber = jobNumber
        user.updateUser = updateUser
        user.save()
        return JSONResponse('true', status=200)
    return JSONResponse('page not found', status=404)
        

# 删除用户
@csrf_exempt
def delete(request, userId):
    if request.method == 'GET':
        user = isUser(userId)
        user.delete()
        return JSONResponse('true', status=200)
    return JSONResponse('page not found', status=404)



# 生成时间戳