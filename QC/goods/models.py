from django.db import models

# Create your models here.

#  商品明细表
# class GoodsItem(models.Model):
#     barCode = models.CharField(max_length=20,null=True,unique=True) # 不可重复
#     supplierCode = models.CharField(max_length=20)
#     supplierName = models.CharField(max_length=50)
#     purchaseCode = models.CharField(max_length=20)
#     purchaseRow = models.CharField(max_length=10,blank=True)
#     orderNo = models.CharField(max_length=20)
#     salebindCode = models.CharField(max_length=20,null=True,blank=True)
#     productCode = models.CharField(max_length=20)
#     productName = models.CharField(max_length=100)
#     sizeDesc = models.CharField(max_length=200,blank=True)
#     customizedCode = models.CharField(max_length=20,blank=True)
#     orderDate = models.DateTimeField(default="1999-01-01")    
#     recDate = models.DateTimeField(default="1999-01-01")
#     number = models.IntegerField(default=0)
#     styleCode = models.CharField(max_length=20,null=True)
#     styleName = models.CharField(max_length=20,null=True)
#     seriesCode = models.CharField(max_length=20)
#     seriesName = models.CharField(max_length=50)
#     typeCode = models.CharField(max_length=20)
#     typeName = models.CharField(max_length=50)    
#     createDate = models.DateTimeField(auto_now_add=True)
#     createUser = models.CharField(max_length=20)
#     updateDate = models.DateTimeField(auto_now=True)
#     updateUser = models.CharField(max_length=20,null=True)
#     class Meta:
#         db_table = 'goodsItem'