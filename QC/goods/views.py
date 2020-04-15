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

from . import updateGoods

class JSONResponse(HttpResponse):
    """
        自定义http返回的内容
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# 获取商品详细信息
@csrf_exempt
def getGoodsItem(request,barcode):
    if request.method == 'GET':
        try:
            goodsItem = models.GoodsItem.objects.get(barCode=barcode)
        except models.GoodsItem.DoesNotExist:
            return HttpResponse('not find',status=404)
        serializer = serializers.GoodsItemSeralizer(goodsItem)

        return JSONResponse(serializer.data)    
    return HttpResponse(status=404)


# 获取所有的产品类别表
@csrf_exempt
def getAllGoodsType(request):
    if request.method == 'GET':
        try:
            goodsType = models.GoodsType.object.all()
        except models.GoodsType.DoesNotExist:
            return HttpResponse('not find',status=404)
        serializer = serializers.GoodsTypeSeralizer(goodsType,many=True)
        return JSONResponse(serializer.data) 
    return HttpResponse(status=404)


# 测试接口
@csrf_exempt    
def test(request):
    # print('666')
    data = request.POST
    print(data)
    newdata = data.dict()
    print('newdata',newdata)
    for i in newdata:
        print('i',i)
    # q = data['0[name]']
    # print('q',q)

    return HttpResponse('success!!')


@csrf_exempt 
def updataGoods(request):
    
    updateGoods.updateGoodsInfo()
    return HttpResponse('hello')