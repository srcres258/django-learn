# 在这里自定义模板标签
# 官方文档：https://docs.djangoproject.com/zh-hans/5.1/howto/custom-template-tags/

from django import template
from blog.models import Category

register = template.Library()

@register.simple_tag
def get_category_list():
    return Category.objects.all()