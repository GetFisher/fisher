from django.db import models
from userinfo.models import *
from sale.models import *
# Create your models here.
ORDERSTATUS = (
    (0,'已出价'),
    (1,'已支付'),
    (2,'交易成功'),
    (3,'订单关闭'),
    (4,'交易中'),
)


# 意愿表
class Cart(models.Model):
    buser = models.ForeignKey(UserInfo)
    car = models.ForeignKey(Carinfo)
    price = models.DecimalField('出价',max_digits=10,decimal_places=2)


class Order(models.Model):
    sale_user = models.ForeignKey(UserInfo,related_name='suser')
    buy_user = models.ForeignKey(UserInfo,related_name='buser')
    brand = models.CharField('车辆信息',max_length=200,null=False)
    price = models.DecimalField('出价',max_digits=10,decimal_places=2)
    orderStatus = models.IntegerField('订单状态',choices=ORDERSTATUS,default=0)
    orderNo = models.CharField('订单号',max_length=50,null=False)
    isDelete = models.BooleanField('是否删除',default=False)

    def __str__(self):
        return self.orderNo

