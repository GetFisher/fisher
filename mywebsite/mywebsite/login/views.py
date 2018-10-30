import logging

from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.db import DatabaseError
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from main_page.models import *
# Create your views here.


def register_views(request):
    if request.method == "POST":
        new_user = Userinfo()
        new_user.username = request.POST.get('username')
        olduser = Userinfo.objects.filter(username=new_user.username)
        if olduser:
            return render(request, "register.html", {"msg": "用户名已存在"})
        if request.POST.get('password') != request.POST.get('cpassword'):
            return render(request, "register.html", {"msg": "密码不一致"})
        new_user.password = make_password(request.POST.get('password'), None, 'pbkdf2_sha1')
        print(request.POST.get('email',None))
        print(request.POST.get('phone', None))
        if request.POST.get('email'):
            new_user.email = request.POST.get('email')
        else:
            return render(request, "register.html", {"msg": "邮箱没输入"})
        if request.POST.get('phone') and len(request.POST.get('phone')) == 11:
            new_user.uphone = request.POST.get('phone')
        else:
            return render(request, "register.html", {"msg": "电话有问题"})
        try:
            new_user.save()
        except DatabaseError as e:
            logging.warning(e)
        return redirect('/')
    elif request.method == "GET":
        return render(request, "register.html")

# def login_views(request):
#     if request.method == 'GET':
#         # 判断缓存中是否有cookie
#         if 'uname' in request.COOKIES and 'uid' in request.COOKIES:
#             return render(request, 'index.html')
#         # 判断是否有session
#         if 'uname' in request.session and 'uid' in request.session:
#             uname = request.session['uname']
#             uid = request.session['uid']
#             # 从session中获取值赋予cookie
#             resp = render_to_response('index.html', {})
#             resp.set_cookie('uname', uname)
#             resp.set_cookie('uid', uid)
#             return resp
#         return render(request, 'login.html')
#     if request.method == 'POST':
#         uname = request.POST.get('username')
#         upwd = request.POST.get('password')
#         try:
#             list = Userinfo.objects.get(uname=uname)
#             uid = list.id
#             if list:
#                 if list.upwd != upwd:
#                     msg = '密码错误'
#                     return render(request, 'login.html', locals())
#                 else:
#                     resp = render_to_response('index.html', {})
#                     resp.set_cookie('uname', uname)
#                     resp.set_cookie('uid', uid)
#                     request.session['uname'] = uname
#                     request.session['uid'] = str(uid)
#                     return resp
#         except BaseException as e:
#             print(e)
#             msg = '账号不存在'
#             return render(request, 'login.html', locals())
def login_views(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {"msg": "用户名密码错误"})
    elif request.method == "GET":
        return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')
