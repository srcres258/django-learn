from django.contrib import admin
from django.forms import widgets
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import SafeData

# Register your models here.
from .models import Category, Post, Tag, Sidebar


for model in [Category, Tag, Sidebar]:
    admin.site.register(model)


class PostAdmin(admin.ModelAdmin):
    """文章详情管理"""

    list_display = ('id', 'title', 'category', 'tags', 'owner', 'pv', 'is_hot', 'pub_date')
    list_filter = ('owner',)
    search_fields = ('title', 'desc')
    list_editable = ('is_hot',)
    list_display_links = ('id', 'title')

    class Media:
        css = {
            'all': ('ckeditor5/cked.css',)
        }
        js = (
            'jquery.js',
            'ckeditor5/ckeditor.js',
            'ckeditor5/translations/zh.js',
            'ckeditor5/config.js'
        )


admin.site.register(Post, PostAdmin)