from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
SEX_CHOICES = (
    (0,'男'),
    (1,'女'),
)

CARDSTATUS = (
    (0,'冻结'),
    (1,'未审核'),
    (2,'已审核'),
    (3,'已删除'),
)

class UserInfo(AbstractUser):
    cellphone = models.CharField('手机号',max_length=20,null=False)
    realname = models.CharField('真实姓名',max_length=30,null=False)
    uidentity = models.CharField('身份证',max_length=50,null=False)
    address = models.TextField('地址')
    sex = models.IntegerField('性别',choices=SEX_CHOICES,default=0)

    def __str__(self):
        return self.username


class Bank(models.Model):
    bank = models.CharField('开户行',max_length=50,null=False)
    cardNo = models.CharField('卡号',max_length=30,null=False)
    cardStatus = models.IntegerField('银行卡状态',choices=CARDSTATUS,default=1)
    user = models.ForeignKey(UserInfo)

    def __str__(self):
        return self.user.realname

class Message(models.Model):
    message = models.CharField('消息',max_length=200,null=False)
    user = models.ForeignKey(UserInfo)
    date = models.DateTimeField('时间',auto_now=True)

    def __str__(self):
        return self.user.realname
