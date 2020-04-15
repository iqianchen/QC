from . import models
from rest_framework import serializers

# 定义序列化
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ('id','userId','name','type','position','avatar','jobNumber','openId','createUser','createDate','updateUser','updateDate')


class GoodsItemSeralizer(serializers.ModelSerializer):
    class Meta:
        model = models.GoodsItem
        fields = ('id','barCode','supplierCode','supplierName','purchaseCode','purchaseRow','orderNo','salebindCode','productCode','productName','sizeDesc','customizedCode','orderDate','recDate','number','styleCode','styleName','seriesCode','seriesName','typeCode','typeName','createDate','createUser','updateDate','updateUser') 


class GoodsTypeSeralizer(serializers.ModelSerializer):
    class Meta:
        model = models.GoodsType
        fileds = ('id','typeCode','typeName','createDate','createUser','updateDate','updateUser')