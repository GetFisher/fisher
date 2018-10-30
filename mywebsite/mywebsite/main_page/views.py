import json
import random

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from goodss.models import *
# Create your views here.
from django.views.decorators.csrf import csrf_protect


# 主页,查询文章显示主页(查询最新的5页)
def main_page_views(request):
    all = []
    # 板块顶部随机一篇文章
    n = random.randint(1, 6)
    art = 'view/'+str(Article.objects.filter(id=n)[0].id)
    # 推荐文章浏览率展示文章10篇(title，id)
    artn_list = []
    artn = Article.objects.all().order_by('-ascanning')[:10]
    n = 1
    for i in artn:
        dic1 = {
            'n': n,
            'url': '/view/'+str(i.id) + '/',
            'title': i.title,
        }
        n += 1
        artn_list.append(dic1)
    # 随机图片展示3
    pictures = Picture.objects.filter().order_by('-id')[:3]
    all_pic = []
    for i in pictures:
        dic = {
            'title': i.ptitle,
            'img': i.imgurl.__str__()[9:],
        }
        all_pic.append(dic)
    # 随机商品展示9

    # 主体文章，最新5篇
    article = Article.objects.filter().order_by('-id')[:5]
    for i in article:
        dic = {
            'title': i.title,
            'content': i.content[:150],
            'postdate': i.postdate,
            'picture': i.picture.__str__()[9:],
            'scanning': i.ascanning,
            'url': '/view/'+str(i.id) + '/',
            'type': i.atype
        }
        all.append(dic)
    return render(request, 'index.html', locals())


# 详情页
def view_views(request, id):
    picture = Picture.objects.all()[0].imgurl.__str__()[9:]
    # print(picture)
    try:
        artical = Article.objects.get(id=id)
    except Exception as e:
        return redirect('/')
    contents = artical.content.split('\n')
    dic = {
        'title': artical.title,
        'content': contents,
        'postdate': artical.postdate,
        'picture': artical.picture.__str__()[9:],
        'scanning': artical.ascanning,
    }
    # 推荐文章浏览率展示文章10篇(title，id)
    artn_list = []
    artn = Article.objects.all().order_by('-ascanning')[:10]
    n = 1
    for i in artn:
        dic1 = {
            'n': n,
            'url': '/view/' + str(i.id) + '/',
            'title': i.title,
        }
        n += 1
        artn_list.append(dic1)
    # 图文并茂显示
    pictures = Picture.objects.filter().order_by('-id')[:3]
    all_pic = []
    for i in pictures:
        dic2 = {
            'title': i.ptitle,
            'img': i.imgurl.__str__()[9:],
        }
        all_pic.append(dic2)
    return render(request, 'picture.html', locals())


# 图片展示页
def show_pict(request):
    pictures = Picture.objects.filter().order_by('-id')[0:6]
    all = []
    for i in pictures:
        dic = {
            'title': i.ptitle,
            'img': i.imgurl.__str__()[9:],
        }
        all.append(dic)
    return render(request, 'show_picture.html', locals())


#商店展示
def show_goods(request):
    if 'sessionid' in request.COOKIES and 'csrftoken' in request.COOKIES:
        good_list = Goods.objects.filter().order_by('-id')[:20]
        all = []
        for i in good_list:
            dic = {
                'img': '/static/' + i.gpicture.__str__(),
                'name': i.gname,
                'price': i.gprice,
            }
            all.append(dic)

        return render(request, 'show_goods.html', locals())
    else:
        return render(request, 'login.html')


