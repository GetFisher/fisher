import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *


# Create your views here.
def index_views(request):
    return render(request, 'index.html')


# /login 对应的视图
# 根据流程图分情况判断
def login_views(request):
    if request.method == 'GET':
        # get流程
        # 判断session中是否有登录信息
        if 'uid' in request.session and 'uphone' in request.session:
            # session中有值
            # 重定向回首页或原路径
            return redirect('/login/')
        else:
            # session中没有值
            # 判断cookie的值
            # 有值
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                # 从cookies中取出数据保存入session中，确保登录状态,再重定向回去
                # ｃｏｏｋｉｅ取值
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                # ｓｅｓｓｉｏｎ赋值
                request.session['uid'] = uid
                request.session['uphone'] = uphone
                return redirect('/login/')
            else:
                # cookies中没有信息,去往登录页面
                form = LoginForm()
                return render(request, 'login.html', locals())
    # POST流程
    else:
        #　通过传递过来的值对数据库进行查询操作
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        ulist = Users.objects.filter(uphone=uphone, upwd=upwd)
        print(uphone, upwd)
        print(ulist)
        if ulist:
            # ulist 存在登录成功,存入session
            uid = ulist[0].id
            request.session['uphone'] = uphone
            request.session['uid'] = uid
            resp = redirect('/')
            # 判断是否记录登录状态,cookies
            if 'isSaved' in request.POST:
                # 记住密码被选定
                resp.set_cookie('uid', uid, 60*60*24*366)
                resp.set_cookie('uphone', uphone, 60*60*24*366)
            return resp
        else:
            # 登录失败,form为通过模块生成的注册控件，需要传递回登录网址填充页面
            form = LoginForm()
            errMsg = 'no'
            return render(request, 'login.html', locals())


# /register 对应的视图
def register_views(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 实现注册功能
        # uphone = request.POST['uphone']
        # uname = request.POST['uname']
        # upwd = request.POST['upwd']
        # uemail = request.POST['uemail']
        # Users.objects.create(uphone=uphone, uname=uname, upwd=upwd, uemail=uemail).save()  # 可选
        dic = {
            "uphone": request.POST['uphone'],
            "uname": request.POST['uname'],
            "upwd": request.POST['upwd'],
            "uemail": request.POST['uemail']
        }
        # 数据插入数据库
        Users(**dic).save()
        # 根据电话的值再查询数据库
        u = Users.objects.get(uphone=request.POST['uphone'])
        # 将用户id和uphone保存进session
        request.session['uid'] = u.id
        request.session['uphone'] = u.uphone
        return redirect('/')

# 验证手机号是否存在
def checkuphone_views(request):
    if request.method == 'POST':
        uphone = request.POST['uphone']
        ulist = Users.objects.filter(uphone=uphone)
        # 如果存在则返回状态码0，和提示信息
        if ulist:
            dic = {
                "status": 0,
                "text": "手机号码已经存在"
            }
            # return HttpResponse(json.dumps(dic))
        # 如果不存在则返回状态码4，和提示信息
        else:
            dic = {
                "status": 1,
                "text": "可以注册"
            }
        return HttpResponse(json.dumps(dic))


def checklogin_views(request):
    # 判断用户会话中是否有登录信息
    if 'uid' in request.session and 'uphone' in request.session:
        # 根据uid 获取uname的值
        uid = request.session['uid']
        # 根据uid查询出对应的user信息转换成字典，响应给客户端
        user = Users.objects.get(id=uid)
        jsonstr = json.dumps(user.to_dict())
        dic = {
            "status": 1,
            "user": jsonstr
        }
        return HttpResponse(json.dumps(dic))
    # session没有登录信息
    else:
        # 判断cookie是否有登录信息
        if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
            # 从cookie中取出数据保存入session
            uid = request.COOKIES['uid']
            uphone = request.COOKIES['uphone']
            request.session['uid'] = uid
            request.session['uphone'] = uphone
            # 根据uid查询出对应的user信息转换成字典，响应给客户端
            user = Users.objects.get(id=uid)
            jsonstr = json.dumps(user.to_dict())
            dic = {
                "status": 1,
                "user": jsonstr
            }
            return HttpResponse(json.dumps(dic))
        else:
            dic = {
                "status": 0,
                "text": "用户尚未登录"
            }
            return HttpResponse(json.dumps(dic))


# 退出登录，清空浏览器临时数据session\cookie,原路返回
def logout_views(request):
    # 判断原始路径，若无则返回主页
    url = request.META.get("HTTP_REFERER", '/')
    resp = redirect(url)
    if 'uid' in request.session and 'uphone' in request.session:
        del request.session['uid']
        del request.session['uphone']
    if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
        resp.delete_cookie('uid')
        resp.delete_cookie('uphone')
    return resp


# 查询所有商品类型，和对应商品的十条信息
def loadgoods_views(request):
    all_list = []
    types = GoodsType.objects.all()
    for type in types:
        # 将得到的对象转换成json字符串
        type_json = json.dumps(type.to_dict())
        # 获取type下所有的商品(前十个)
        g_list = type.goods_set.order_by('-price')[0:10]
        g_list_json = serializers.serialize('json', g_list)
        dic = {
            "type": type_json,
            "goods": g_list_json,
        }
        all_list.append(dic)
    return HttpResponse(json.dumps(all_list))


# 添加或更新数量到购物车
def add_cart_views(request):
    users_id = request.session['uid']
    print(users_id)
    goods_id = request.GET['goods_id']
    print(goods_id)
    # 接收购买的数量，如果没有则默认为１
    ccount = request.GET.get('ccount', 1)
    # 查看购物车中是否有相同用户购买过相同商品，如果有则更新数量，没有则新增数据
    cartlist = CartInfoo.objects.filter(user_id_id=users_id, goods_id_id=goods_id)
    print(cartlist)
    if cartlist:
        #更新商品
        cartinfo = cartlist[0]
        cartinfo.count = cartinfo.count + int(ccount)
        cartinfo.save()
        dic = {
            'status': 1,
            'text': '更新数量成功!'
        }
        return HttpResponse(json.dumps(dic))
    else:
        # 创建一条记录并存入数据库
        cartinfo = CartInfoo()
        cartinfo.user_id_id = users_id
        cartinfo.goods_id_id = goods_id
        cartinfo.count = int(ccount)
        cartinfo.save()
        dic = {
            'status': 1,
            'text': '添加至购物车成功!'
        }
        return HttpResponse(json.dumps(dic))

# 显示用户购物车数量
def cart_count_views(request):
    if 'uid' not in request.session:
        dic = {
            'count': 0
        }
        return HttpResponse(json.dumps(dic))
    else:
        uid = request.session['uid']
        all_cart =CartInfoo.objects.filter(user_id_id=uid)
        total_count = 0
        for cart in all_cart:
            total_count += cart.count
        dic = {
            'count': total_count
        }
        return HttpResponse(json.dumps(dic))