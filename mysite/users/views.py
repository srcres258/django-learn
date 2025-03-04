from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate
from .forms import LoginForm, RegisterForm

# Create your views here.

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

def register(request):
    """注册视图"""

    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.save()

            return HttpResponse('注册成功')

    context = {'form': form}
    return render(request, 'users/register.html', context)
