from django.db import models
from userinfo.models import *
# Create your models here.
EXAMINE = (
    (0,'审核中'),
    (1,'审核通过'),
    (2,'审核不通过'),
)



class Brand(models.Model):
    btitle = models.CharField('品牌名称',max_length=50,null=False)
    logo_brand = models.ImageField('logo',upload_to='img/logo',default='')
    isDelete = models.BooleanField('是否删除',default=False)

    def __str__(self):
        return self.btitle


class Carinfo(models.Model):
    serbran = models.ForeignKey(Brand)
    user = models.ForeignKey(UserInfo)
    ctitle = models.CharField('车名',max_length=30,null=False)
    regist = models.DateField('上牌日期',null=False)
    enginNo = models.CharField('发动机号',max_length=50,null=False)
    mileage = models.IntegerField('公里数',default=0)
    price = models.DecimalField('价格',decimal_places=2,max_digits=10)
    color = models.CharField('颜色',max_length=10,null=True)
    maintenance = models.CharField('维修记录',max_length=200,null=True)
    extractprice = models.DecimalField('成交价格',decimal_places=2,max_digits=10)
    newprice = models.DecimalField('新车价格',decimal_places=2,max_digits=10)
    picture = models.ImageField('汽车图片',upload_to='img/car',default='')
    formalities = models.BooleanField('手续是否齐全',default=True)
    debt = models.BooleanField('是否有债务',default=False)
    promise = models.TextField('卖家承诺',null=True)
    examine = models.IntegerField('审核进度',choices=EXAMINE,default=0)
    isPurchase = models.BooleanField('是否购买',default=False)
    isDelete = models.BooleanField('是否删除',default=False)

    def __str__(self):
        return self.enginNo