from django.shortcuts import render
from django.contrib.auth.hashers import make_password,check_password
from .models import *
from django.db import DatabaseError
import logging
from django.contrib import auth

# Create your views here.
# 注册
def register_(request):
    # 1判断post/get
    # 2get返回注册页
    # 3post
    #     获取数据
    #     判断用户名是否存在
    #         存在：返回注册页
    #         不存在：
    #             判断密码是否一致
    #             密码加密
    #             保存用户
    #     判断买车卖车
    #         买车：首页
    #         卖车：完善卖车信息
    #
    if request.method=="POST":
        new_user = UserInfo()
        new_user.username = request.POST.get('username')
        olduser = UserInfo.objects.filter(username=new_user.username)
        if olduser:
            return render(request,"register.html",{"msg":"用户名已存在"})
        if request.POST.get('pwd') != request.POST.get('cpwd'):
            return render(request,"register.html",{"msg":"密码不一致"})
        new_user.password = make_password\
    (request.POST.get('pwd'),None,'pbkdf2_sha1')
        try:
            new_user.save()
        except DatabaseError as e:
            logging.warning(e)
        if 'tobuy' in request.POST:
            return render(request,"index.html")
        elif 'tosale' in request.POST:
            return render(request,"info-message.html")

    elif request.method == "GET":
        return render(request,"register.html")


def login_(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user = auth.authenticate\
            (username=username,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return render(request,"info-message.html")
        else:
            return render(request,'login.html',{"msg":"用户名密码错误"})
    elif request.method == "GET":
        return render(request,"login.html")


def logout(request):
    auth.logout(request)
    return render(request,"index.html")


def salecar(request):
    # 1post/get
    # 2获取信息:用户基础信息userinfo
    #         所卖车型信息carinfo
    # (下拉列表，单选，图片)
    # 3保存
    # cellphone
    # realname
    # uidentity
    # address
    # sex
    #
    # serbran = models.ForeignKey(Brand)
    # user = models.ForeignKey(UserInfo)
    # ctitle = models.CharField('车名',max_length=30,null=False)
    # regist = models.DateField('上牌日期',null=False)
    # enginNo = models.CharField('发动机号',max_length=50,null=False)
    # mileage = models.IntegerField('公里数',default=0)
    # price = models.DecimalField('价格',decimal_places=2,max_digits=10)
    # color = models.CharField('颜色',max_length=10,null=True)
    # maintenance = models.CharField('维修记录',max_length=200,null=True)
    # extractprice = models.DecimalField('成交价格',decimal_places=2,max_digits=10)
    # newprice = models.DecimalField('新车价格',decimal_places=2,max_digits=10)
    # picture = models.ImageField('汽车图片',upload_to='img/car',default='')
    # formalities = models.BooleanField('手续是否齐全',default=True)
    # debt = models.BooleanField('是否有债务',default=False)
    # promise = models.TextField('卖家承诺',null=True)
    # examine = models.IntegerField('审核进度',choices=EXAMINE,default=0)
    # isPurchase = models.BooleanField('是否购买',default=False)
    # isDelete = models.BooleanField('是否删除',default=False)
    #brands sex pic
    pass






