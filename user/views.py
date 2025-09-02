# user的views.py
from django.shortcuts import render, redirect
from django.shortcuts import reverse
from user.models import *
from .form import MyUserCreationForm
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password


# 用户注册与登录
def loginView(request):
    user = MyUserCreationForm()
    # 提交表单
    if request.method == 'POST':
        # 判断提交的是用户登录还是用户注册
        # 用户登录
        if request.POST.get('loginUser', ''):
            u = request.POST.get('loginUser', '')
            p = request.POST.get('password', '')
            ul = MyUser.objects.filter(Q(mobile=u) | Q(username=u)).first()
            if check_password(p, ul.password):
                login(request, ul)
                return redirect(reverse(
                    'comment', kwargs={'page': 1}))
            else:
                tips = '密码错误'
        else:
            tips = '用户不存在'
        # 用户注册
        else:
        u = MyUserCreationForm(request.POST)
        if u.is_valid():
            u.save()
            tips = '注册成功'
        else:
            if u.errors.get('username', ''):

                tips = u.errors.get('username', '注册失败')
            else:
                tips = u.errors.get('mobile', '注册失败')


     return render(request, 'user.html', locals())
# Create your views here.
