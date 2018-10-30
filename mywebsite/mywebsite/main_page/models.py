
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.template.backends import django
from django.utils import timezone


class Userinfo(AbstractUser):
    uname = models.CharField(max_length=30, verbose_name='真实姓名', null=False)
    upwd = models.CharField(max_length=20, verbose_name='用户初级密码', null=False)
    uemail = models.EmailField(null=True, verbose_name='邮箱')
    uphone = models.CharField(max_length=11, verbose_name='手机号码', null=False)
    address = models.TextField(null=False, default='')
    ctime = models.DateField('创建时间', default=timezone.now)

    def __str__(self):
        return self.uname

    class Meta:
        db_table = 'userinfo'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class Picture(models.Model):
    ptitle = models.CharField('图片标题', max_length=50, null=False)
    imgurl = models.ImageField(upload_to='main_page/static/pimg', null=False)

    def __str__(self):
        return self.ptitle

    class Meta:
        db_table = 'my_picture'
        verbose_name = '图片管理'
        verbose_name_plural = verbose_name

class Article(models.Model):
    title = models.CharField('标题', max_length=20, null=False)
    atype = models.CharField('文章类型', max_length=20, null=False)
    content = models.TextField('文章内容', null=False)
    picture = models.ImageField('文章配图', upload_to='main_page/static/aimg', default='')
    postdate = models.DateField('上传日期', default=timezone.now)
    astatus = models.BooleanField('是否展示', )
    ascanning = models.IntegerField('浏览量', default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name