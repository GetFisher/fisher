from django.db import models

# Create your models here.

class Users(models.Model):
    uphone = models.CharField(max_length=20, verbose_name='手机号')
    upwd = models.CharField(max_length=20, verbose_name='密码')
    uemail = models.EmailField(verbose_name='邮箱')
    uname = models.CharField(max_length=20, verbose_name='用户名')
    isActive = models.BooleanField(default=True, verbose_name='激活状态')

    def __str__(self):
        return self.uname

    def to_dict(self):
        dic = {
            "uphone": self.uphone,
            "upwd": self.upwd,
            "uname": self.uname,
            "uemail": self.uemail,
            "isActive": self.isActive
        }
        return dic


    class Meta:
        verbose_name = '用户名'
        verbose_name_plural = verbose_name


class GoodsType(models.Model):
    # 创建商品类型的实体
    title = models.CharField(max_length=50, verbose_name='类型名称')
    # 商品类型的图片
    picture = models.ImageField(upload_to='static/upload/goodstype', null=True, verbose_name='类型图片')
    # 商品类型的描述
    desc = models.TextField(verbose_name='商品描述')

    def to_dict(self):
        dic = {
            "title": self.title,
            "picture": self.picture.__str__(),
            "desc": self.desc
        }
        return dic

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'GoodsType'
        verbose_name = '商品类型'
        verbose_name_plural = verbose_name


class Goods(models.Model):
    title = models.CharField(max_length=30, verbose_name="商品名称")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='商品价格')
    spec = models.CharField(max_length=20, verbose_name='商品规格')
    picture = models.ImageField(upload_to='static/upload/goods', verbose_name='商品图片', null=True)
    goodsType = models.ForeignKey(GoodsType, verbose_name='商品类型')
    isActive = models.BooleanField(verbose_name='状态', default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'goodsType'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class CartInfoo(models.Model):
    user_id = models.ForeignKey(Users, verbose_name='user_id')
    goods_id = models.ForeignKey(Goods, verbose_name='good_id')
    count = models.IntegerField(verbose_name='购买数量')

    def __str__(self):
        return '用户' + str(self.user_id) + ':购物情况'