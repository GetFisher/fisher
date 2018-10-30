from django.db import models

# Create your models here.
from django.db import models
from main_page.models import *

GOOGDSTATUS = (
    (1, '上架'),
    (2, '审核'),
    (3, '下架'),
    (4, '非卖品')
)


class Goods(models.Model):
    gname = models.CharField('商品名称', max_length=50, null=False)
    gtype = models.CharField('商品类型', max_length=50, null=True)
    gdesc = models.TextField('商品描述', null=True)
    units = models.CharField('单位', max_length=20, null=False)
    gpicture = models.ImageField('商品图片', upload_to='gimg')
    gprice = models.DecimalField('商品价格', max_digits=10, decimal_places=2, null=False)
    gstatus = models.IntegerField('商品状态', choices=GOOGDSTATUS, default=2)

    def __str__(self):
        return self.gname

    def get_goodstatus(self):
        if self.gstatus == 1:
            return '上架'
        if self.gstatus == 1:
            return '审核'
        if self.gstatus == 1:
            return '下架'
        if self.gstatus == 1:
            return '非卖品'

    class Meta:
       db_table = 'goods'
       verbose_name = '商品管理'
       verbose_name_plural = verbose_name


class Cart(models.Model):
    cuid = models.ForeignKey(Userinfo, on_delete=models.DO_NOTHING, verbose_name='购买用户')
    cgid = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, verbose_name='购买的商品')
    ccount = models.IntegerField('购买数量', null=False)
    totalprice = models.DecimalField('总价', max_digits=10, decimal_places=2)
    cstastus = models.BooleanField('购物车状态', default=False)

    def __str__(self):
        return self.cuid.uname

    class Meta:
        db_table = 'cart'
        verbose_name = '购物车管理'
        verbose_name_plural = verbose_name


ORDERSTATUS = (
    (1, '等待支付'),
    (2, '已支付'),
    (3, '订单已取消')
)


class Order(models.Model):
    orderno = models.CharField('订单号码', max_length=80, null=False)
    ouid = models.ForeignKey(Userinfo, on_delete=models.DO_NOTHING, verbose_name='购买用户')
    ogid = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, verbose_name='购买的商品')
    ocals = models.TextField('商品订单详细', null=False)
    address = models.CharField('送货地址地址', max_length=200, null=False)
    ostatus = models.IntegerField('订单状态', choices=ORDERSTATUS, default=1)

    def get_orderstatus(self):
        if self.ostatus == 1:
            return '等待支付'
        if self.ostatus == 1:
            return '已支付'
        if self.ostatus == 1:
            return '订单已取消'

    class Meta:
        db_table = 'order'
        verbose_name = '订单管理'
        verbose_name_plural = verbose_name
