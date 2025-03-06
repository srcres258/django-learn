from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserForm, UserProfileForm
from .models import EmailVerifyRecord, UserProfile
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
                # 登录成功之后跳转到个人中心页面
                return redirect('users:user_profile')
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

def forget_pwd(request):
    """忘记密码视图"""

    if request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            exists = User.objects.filter(email=email).exists()
            if exists:
                send_register_email(email, 'forget')
                return HttpResponse('重置密码邮件已发送，请注意查收！')
            else:
                return HttpResponse('邮箱还不存在，请前往注册！')
    else:
        form = ForgetPwdForm()

    return render(request, 'users/forget_pwd.html', {'form': form})

def forget_pwd_url(request, active_code):
    """修改密码视图"""

    if request.method == 'POST':
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.username = email
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()

            return HttpResponse('密码修改成功，请使用新密码登录！')
        else:
            return HttpResponse('密码修改失败，验证码错误或密码不符合要求！')
    else:
        form = ModifyPwdForm()

    return render(request, 'users/reset_pwd.html', {'form': form})

@login_required(login_url='users:login')
def user_profile(request):
    """用户中心视图"""

    user = User.objects.get(username=request.user)
    return render(request, 'users/user_profile.html', {'user': user})

def logout_view(request):
    """登出视图"""

    logout(request)
    return redirect('users:login')

def editor_users(request):
    """编辑用户信息视图"""

    # 逻辑在这里
    user = User.objects.get(id=request.user.id) # 当前登录用户

    if request.method == 'POST':
        try:
            # 如果UserProfile存在。
            user_profile = user.userprofile # 如果这一块的数据不存在，会引发一个错误。

            # 真正的保存逻辑在这里。

            # 保存加修改的一个操作，instance默认显示他原有的数据。
            form = UserForm(request.POST, instance=user)
            # UserProfile和User之间是一个一对一关系，默认注册的时候是没有数据的，注册成功之后，他才会在个人中心设置信息。
            # 第一次登录的话应该是空表单，如果设置了数据，那以后编辑的话就是修改，应该要默认显示原有的数据。
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()

                return redirect('users:user_profile')
        except UserProfile.DoesNotExist: # 这里发生错误说明 UserProfile 无数据。
            form = UserForm(request.POST, instance=user) # 填充默认数据给当前用户。
            user_profile_form = UserProfileForm(request.POST, request.FILES) # 空表单，直接获取空表单的数据保存。

            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据。
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = user
                new_user_profile.save()

                return redirect('users:user_profile')
    else:
        try:
            # 如果UserProfile存在。
            user_profile = user.userprofile # 如果这一块的数据不存在，会引发一个错误。

            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=user_profile)


        except UserProfile.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()

    return render(request, 'users/editor_users.html', locals())
