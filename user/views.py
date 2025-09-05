"""
    路由login将实现用户注册与登录功能，路由的HTTP请求由视图函数loginView负责接收和处理。
"""

# user的views.py
# user的views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from index.models import Dynamic
from user.models import *
from .form import MyUserCreationForm

# 用户注册与登录
def loginView(request):
    user = MyUserCreationForm()
    tips = ''
    if request.method == 'POST':
        # 登录
        if request.POST.get('loginUser', '') is not None:
            login_user = request.POST.get('loginUser', '').strip()
            password = request.POST.get('password', '')
            # 使用Django内置认证系统
            user = authenticate(request, username=login_user, password=password)
            if user is not None:
                login(request, user)
                # 登录成功后跳转到首页
                return redirect(reverse('index'))
            else:
                # 尝试通过手机号或用户名查找
                account = MyUser.objects.filter(Q(mobile=login_user) | Q(username=login_user)).first()
                if not account:
                    tips = '用户不存在'
                else:
                    if check_password(password, account.password):
                        login(request, account)
                        return redirect(reverse('index'))
                    else:
                        tips = '密码错误'
        # 注册
        else:
            form = MyUserCreationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                tips = '注册成功'
            else:
                if form.errors.get('username', ''):
                    tips = form.errors.get('username', '注册失败')
                else:
                    tips = form.errors.get('mobile', '注册失败')
    # GET 请求渲染空表单
    return render(request, 'login.html', locals())

# 用户中心
# 设置用户登录限制
@login_required(login_url='/user/login.html')
def homeView(request, page):
    # 热搜歌曲
    searchs = Dynamic.objects.select_related('song').\
        order_by('-search').all()[:4]
    # 分页功能
    songs = request.session.get('play_list', [])
    paginator = Paginator(songs, 3)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return render(request, 'home.html', locals())

# 退出登录
def logoutView(request):
    logout(request)
    return redirect('/')
