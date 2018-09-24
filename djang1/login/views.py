from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from main_page.models import *
# Create your views here.


def login_views(request):
    if request.method == 'GET':
        # 判断缓存中是否有cookie
        if 'uname' in request.COOKIES and 'uid' in request.COOKIES:
            return render(request, 'index.html')
        # 判断是否有session
        if 'uname' in request.session and 'uid' in request.session:
            uname = request.session['uname']
            uid = request.session['uid']
            # 从session中获取值赋予cookie
            resp = render_to_response('index.html', {})
            resp.set_cookie('uname', uname)
            resp.set_cookie('uid', uid)
            return resp
        return render(request, 'login.html')
    if request.method == 'POST':
        uname = request.POST.get('username')
        upwd = request.POST.get('password')
        try:
            list = Userinfo.objects.get(uname=uname)
            uid = list.id
            if list:
                if list.upwd != upwd:
                    msg = '密码错误'
                    return render(request, 'login.html', locals())
                else:
                    resp = render_to_response('index.html', {})
                    resp.set_cookie('uname', uname)
                    resp.set_cookie('uid', uid)
                    request.session['uname'] = uname
                    request.session['uid'] = str(uid)
                    return resp
        except BaseException as e:
            print(e)
            msg = '账号不存在'
            return render(request, 'login.html', locals())
