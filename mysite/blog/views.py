from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F

from .models import Category, Post

# Create your views here.

def index(request):
    """首页"""

    # 查询首页数据并显示在页面。
    category_list = Category.objects.all() # 查询到所有的分类
    post_list = Post.objects.all() # 查询到所有的文章
    context = { 'category_list': category_list, 'post_list': post_list }
    return render(request, 'blog/index.html', context)

def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    # 获取当前分类下的所有文章。
    posts = category.post_set.all()

    context = { 'category': category, 'post_list': posts }
    return render(request, 'blog/list.html', context)

def post_detail(request, post_id):
    """文章详情页"""

    post = get_object_or_404(Post, id=post_id)

    # # 用文章id来实现的上下篇
    # prev_post = Post.objects.filter(id__lt=post_id).last() # 上一篇的QuerySet数据
    # next_post = Post.objects.filter(id__gt=post_id).first() # 下一篇的QuerySet数据

    # 用发布日期来实现的上下篇（两种方法都可以，任选一个即可）
    prev_post = Post.objects.filter(add_date__lt=post.add_date).last() # 上一篇的QuerySet数据
    next_post = Post.objects.filter(add_date__gt=post.add_date).first() # 下一篇的QuerySet数据

    # 备注：第一篇及最后一篇是没有上下篇的，需要处理url显示。

    # 增加文章浏览量
    Post.objects.filter(id=post_id).update(pv=F('pv') + 1) # **注意**：这个功能有漏洞，仅作思路讲解。

    context = { 'post': post, 'prev_post': prev_post, 'next_post': next_post }
    return render(request, 'blog/detail.html', context)

def search(request):
    """搜索视图"""

    keyword = request.GET.get('keyword')

    if keyword:
        # 包含查询的方法，用Q对象来组合复杂查询， XXX__icontains 他两个之间用的是下划线（__）连接
        post_list = Post.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))
    else:
        # 没有搜索默认显示所有文章
        post_list = Post.objects.all()

    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)

def archives(request, year, month):
    post_list = Post.objects.filter(add_date__year=year, add_date__month=month)
    context = {
        'post_list': post_list,
        'year': year,
        'month': month
    }
    return render(request, 'blog/archives_list.html', context)