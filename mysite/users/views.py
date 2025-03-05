from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

# Create your views here.

from .forms import LoginForm, RegisterForm
from .models import EmailVerifyRecord
from utils.email_send import send_register_email

class MyBackend(ModelBackend):
    """邮箱登录注册"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password): # 加密明文密码
                return user
        except Exception:
            return None

def login_view(request):
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/admin')
            else:
                return HttpResponse('登录失败')

    context = {'form': form}
    return render(request, 'users/login.html', context)

def active_user(request, active_code):
    """修改用户状态，比对链接验证码"""

    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            user = User.objects.get(email=email)
            user.is_staff = True
            user.save()
    else:
        return HttpResponse('链接有误')

    return redirect('users:login')

def register(request):
    """注册视图"""

    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.username = form.cleaned_data.get('email')
            new_user.save()

            # 发送激活邮件
            send_register_email(form.cleaned_data.get('email'), 'register')

            return HttpResponse('注册成功')

    context = {'form': form}
    return render(request, 'users/register.html', context)
