import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User
import hashlib


# Create your views here.

def reg_view(request):
    # 注册
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        if password_1 != password_2:
            # 判断密码是否一致
            return HttpResponse('密码不一致!')
        old_users = User.objects.filter(username=username)
        # 通过hashlib算法加密密码
        m = hashlib.md5()
        m.update(password_1.encode())
        password_m = m.hexdigest()

        if old_users:
            return HttpResponse('用户已注册!')
        try:
            user = User.objects.create(username=username, password=password_m)  # 创建数据
            # 有可能报错，重复插入【唯一索引并发写入问题】
        except Exception as e:
            print(f'登录名错误{e}')
            return HttpResponse('用户名已注册!')

        # 免登录一天
        request.session['username'] = username
        request.session['uid'] = user.id
        # 修改session存储数据为1天

        return HttpResponseRedirect('/index')


def login_view(request):
    # 获取页面
    if request.method == 'GET':
        if request.session.get('username') and request.session.get('uid'):
            # return HttpResponse('已登录')
            return HttpResponseRedirect('/index')
        c_username = request.COOKIES.get('usernaem')
        c_uid = request.COOKIES.get('uid')
        if c_uid and c_username:
            # 诙谐session
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            # return HttpResponse('已登录')
            return HttpResponseRedirect('/index')
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print(f'登录名错误{e}')
            return HttpResponse('用户名或密码错误')
        # 比对密码
        m = hashlib.md5()
        m.update(password.encode())  # 必须encode转化

        if m.hexdigest() != user.password:
            return HttpResponse('用户名或密码错误')

        # 记录会话状态
        request.session['username'] = username
        request.session['uid'] = user.id

        resp = HttpResponseRedirect('/index')
        # 保存用户名免密登录3天,单位为秒，1天为3600*24*1
        if 'remember' in request.POST:
            resp.set_cookie('username', username, 3600 * 24 * 3)
            resp.set_cookie('uid', user.id, 3600 * 24 * 3)
        return resp


def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']

    resp = HttpResponseRedirect('/index')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.session:
        resp.delete_cookie('uid')
    return resp
