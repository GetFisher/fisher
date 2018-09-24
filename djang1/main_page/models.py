from django.db import models

# Create your models here.
from django.template.backends import django
from django.utils import timezone


class Userinfo(models.Model):
    uname = models.CharField(max_length=30, verbose_name='用户名')
    upwd = models.CharField(max_length=20, verbose_name='用户密码')
    uemail = models.EmailField(null=True, verbose_name='邮箱')
    uphone = models.CharField(max_length=11, verbose_name='手机号码')
    address = models.TextField(null=False, default='')
    ctime = models.DateField('创建时间', default=timezone.now)

    def __str__(self):
        return self.uname

    class Meta:
        db_table = '用户信息'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name