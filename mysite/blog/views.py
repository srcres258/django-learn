from django.shortcuts import render

# Create your views here.

def index(request):
    # 查询首页数据并显示在页面。
    return render(request, 'blog/index.html')