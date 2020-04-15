from django.db import models

# Create your models here.

#  用户详情表
class UserInfo(models.Model):
    user_type = (
        (0, '管理员'),
        (1, '检验员')
    )

    userId = models.CharField(max_length=20,unique=True)    # 不可重复
    name = models.CharField(max_length=20)
    type = models.SmallIntegerField(choices=user_type,default=1)
    position = models.CharField(max_length=150,blank=True,null=True)
    avatar = models.CharField(max_length=200,blank=True)
    jobNumber = models.CharField(max_length=15,blank=True,null=True)
    openId = models.CharField(max_length=40,unique=True)    # 不可重复
    createDate = models.DateTimeField()
    createUser = models.CharField(max_length=20)
    createDate = models.DateTimeField(auto_now_add=True)
    updateUser = models.CharField(max_length=20,null=True)
    updateDate = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'userInfo'

#  商品明细表
class GoodsItem(models.Model):
    barCode = models.CharField(max_length=20,null=True,unique=True) # 不可重复
    supplierCode = models.CharField(max_length=20)
    supplierName = models.CharField(max_length=50)
    purchaseCode = models.CharField(max_length=20)
    purchaseRow = models.CharField(max_length=10,blank=True)
    orderNo = models.CharField(max_length=20)
    salebindCode = models.CharField(max_length=20,null=True,blank=True)
    productCode = models.CharField(max_length=20)
    productName = models.CharField(max_length=100)
    sizeDesc = models.CharField(max_length=200,blank=True)
    customizedCode = models.CharField(max_length=20,blank=True)
    orderDate = models.DateTimeField(default="1999-01-01")    
    recDate = models.DateTimeField(default="1999-01-01")
    number = models.IntegerField(default=0)
    styleCode = models.CharField(max_length=20,null=True)
    styleName = models.CharField(max_length=20,null=True)
    seriesCode = models.CharField(max_length=20)
    seriesName = models.CharField(max_length=50)
    typeCode = models.CharField(max_length=20)
    typeName = models.CharField(max_length=50)    
    createDate = models.DateTimeField(auto_now_add=True)
    createUser = models.CharField(max_length=20)
    updateDate = models.DateTimeField(auto_now=True)
    updateUser = models.CharField(max_length=20,null=True)
    class Meta:
        db_table = 'goodsItem'

# 检验项目表
class TestItem(models.Model):
    projectName = models.CharField(max_length=30)
    createDate = models.DateTimeField(auto_now_add=True)
    createUser = models.CharField(max_length=20)
    updateDate = models.DateTimeField(auto_now=True)
    updateUser = models.CharField(max_length=20,null=True)
    class Meta:
        db_table = 'testItem'

# 产品类别表
class GoodsType(models.Model):
    typeCode = models.CharField(max_length=20)
    typeName = models.CharField(max_length=50)
    createDate = models.DateTimeField(auto_now_add=True)
    createUser = models.CharField(max_length=20)
    updateDate = models.DateTimeField(auto_now=True)
    updateUser = models.CharField(max_length=20,null=True)
    class Meta:
        db_table = 'goodsType'

# 类别检验项目表
class GoodsTypeTest(models.Model):
    goodsType = models.ForeignKey(GoodsType, on_delete=models.CASCADE)
    testItem = models.ForeignKey(TestItem, on_delete=models.CASCADE)
    createDate = models.DateTimeField(auto_now_add=True)
    createUser = models.CharField(max_length=20)
    updateDate = models.DateTimeField(auto_now=True)
    updateUser = models.CharField(max_length=20,null=True)  
    class Meta:
        db_table = 'goodsTypeTest'

# 检验项目明细表
class TestItemDetail(models.Model):
    testProject = models.ForeignKey(GoodsType, on_delete=models.CASCADE)
    ordinal = models.IntegerField()
    detail = models.CharField(max_length=200)
    class Meta:
        db_table = 'testItemDetail'

# 检验表
class Test(models.Model):
    test_type = (
        (0, '直验'),
        (1, '分派')
    )

    userId = models.ForeignKey(UserInfo,to_field='userId',db_column='userId',on_delete=models.CASCADE)
    barCode = models.ForeignKey(GoodsItem,to_field='barCode',db_column='barCode',on_delete=models.CASCADE)
    taskNo = models.CharField(max_length=20,null=True)
    testType = models.SmallIntegerField(choices=test_type,default=0)
    desc = models.CharField(max_length=200,null=True)
    testTime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'test'

#  检验明细表
class TestDetail(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    testItem = models.ForeignKey(TestItem, on_delete=models.CASCADE)
    testItemDetail = models.ForeignKey(TestItemDetail, on_delete=models.CASCADE)
    isPass = models.BooleanField()
    class Meta:
        db_table = 'testDetail'

#  检验明细附件表
class TestDetailAttachment(models.Model):
    testDetail = models.ForeignKey(TestDetail, on_delete=models.CASCADE)
    imageUrl = models.CharField(max_length=200)
    class Meta:
        db_table = 'testDetailAttachment'
