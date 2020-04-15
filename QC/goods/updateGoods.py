import pymssql

from user import models
from user import serializers

# 更新商品明细表
def updateGoodsInfo():
    # 打开数据库连接
    db = pymssql.connect(host="10.10.20.150",user="sa",password="cd*'rom08",database="F19_TEST",charset="utf8")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = """select DISTINCT top 5
    f1.fBarcode ,
    b.fprvcode ,
    c.fprvnname,
    a.fPurNo,
    a.flvlcode ,
    a.fordno ,
    e.fsalebindcode ,
    d.fGoodsCode ,
    d.fGoodsName ,
    d.fSizeDesc  ,
    a.fcstlotno ,
    b.fpurdate  ,
    a.frecdate ,
    a.finvqty ,
    f.fStyleCode,
    f.fStyleName ,
    g.fKitCode ,
    g.fKitName ,
    h.fSortCode ,
    h.fSortName
    from   
    t_PURD_PurItem as a 
    left join t_PURD_PurMst as b on a.fPurNo = b.fPurNo     --采购单主表
    left join t_PURM_PrvMst as c on b.fprvcode = c.fprvcode     --供应商资料表
    left join t_BOMM_GoodsMst as d  on a.fGoodsID = d.fGoodsID      --产品资料表
    left join t_COPD_OrdItem as e   on e.fcstlotno = a.fcstlotno and a.fordsno = e.fSNo and a.fordno = e.fOrdNo     --订单细表
    left join t_COPM_StyleMst as f  on d.fStyleCode = f.fStyleCode      --款式资料表
    left join t_COPM_KitMst as g on  g.fKitCode = d.fKitCode        --系列资料表
    left join t_COPM_GoodsSortMst as h on h.fSortCode = d.fSortCode     --产品类别表
    left join v_bcm701_qrybarcodelist as f1 on f1.fOriTypeDesc  = '采购单'      --只取采购条码
    and f1.fPurNo = a.fPurNo and a.fCstLotNo  = f1.fCstLotNo and a.fGoodsID = f1.fGoodsID
    where
    b.fpurdate   >= '2000-01-10' and b.fpurdate <='2018-12-10'
    and b.fCFlag = '1' and  b.fIfClose = '0' and b.fIfCancel   = '0'  
    -- and f1.fBarcode is not null                              
    and d.fGoodsType = '1'                                
    group by b.fprvcode , c.fprvnname,a.fPurNo, a.flvlcode ,a.flvlcode , a.fordno , fsalebindcode , d.fGoodsCode ,d.fGoodsName ,d.fSizeDesc  ,
    a.fcstlotno ,f1.fBarcode , b.fpurdate , a.frecdate , a.finvqty ,f.fStyleCode,f.fStyleName ,g.fKitCode ,g.fKitName ,h.fSortCode ,h.fSortName"""

    try:
        # 执行SQL语句
        # print(sql)
        cursor.execute(sql.encode("utf-8"))
        # print('row',row)
        # 获取所有记录列表
        # print('cursor',dir(cursor))
        results = cursor.fetchone()
        print('results', results)
        # goods = models.GoodsItem.objects.all()
        # goods.delete()
        for row in results:
            print(row)
            try:
                add_data = {
                    'barCode': row[0],
                    'supplierCode': row[1],
                    'supplierName': row[2],
                    'purchaseCode': row[3],
                    'purchaseRow': row[4],
                    'orderNo': row[5],
                    'salebindCode': row[6],
                    'productCode': row[7],
                    'productName': row[8],
                    'sizeDesc': row[9],
                    'customizedCode': row[10],
                    'orderDate': row[11],
                    'recDate': row[12],
                    'number': row[13],
                    'styleCode': row[14],
                    'styleName': row[15],
                    'seriesCode': row[16],
                    'seriesName': row[17],
                    'typeCode': row[18],
                    'typeName': row[19],
                    'createUser': 'admin',
                }
                serializer = serializers.GoodsItemSeralizer(data=add_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
            except:
                pass
            continue
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    print('success')
    db.close()




# 更新商品类别表
def updateGoodsType():
    # 打开数据库连接
    db = pymssql.connect(host="10.10.20.150",user="sa",password="cd*'rom08",database="F19_TEST")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = """select 
    fSortCode, 
    fSortName 
    from
    t_COPM_GoodsSortMst
    where 
    fPSortCode = 'PT'
    """

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('results',results)
        for row in results:
            try:
                add_data = {
                    'typeCode': row[0],
                    'typeName': row[1],
                    'createUser': 'admin'
                }
                serializer = serializers.GoodsTypeSeralizer(data=add_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
            except:
                pass
            continue
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    print('success')
    db.close() 