from django.contrib import admin
from django.forms import widgets
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import SafeData

# Register your models here.
from .models import Category, Post, Tag, Sidebar


for model in [Category, Tag, Sidebar]:
    admin.site.register(model)


def absolute_path(path):
    """
    Given a relative or absolute path to a static asset, return an absolute
    path. An absolute path will be returned unchanged while a relative path
    will be passed to django.templatetags.static.static().
    """
    if path.startswith(("http://", "https://", "/")):
        return path
    return static(path)


class ModuleJS(SafeData):
    __slots__ = ('path',)

    def __init__(self, path: str):
        self.path = path

    def __html__(self):
        return format_html('<script type="module" src="{}"></script>', absolute_path(self.path))


class ImportMapJS(SafeData):
    __slots__ = ('import_map',)

    def __init__(self, import_map: dict[str, str]):
        self.import_map = import_map

    def __html__(self):
        script_content = '{"imports":{'
        for k, v in self.import_map.items():
            script_content += f'"{k}":"{absolute_path(v)}",'
        script_content = script_content[:-1] # 去除尾随逗号，因为JSON标准中不允许出现尾随逗号
        script_content += '}}'

        return f'<script type="importmap">{script_content}</script>'


class PostAdmin(admin.ModelAdmin):
    """文章详情管理"""

    list_display = ('id', 'title', 'category', 'tags', 'owner', 'pv', 'is_hot', 'pub_date')
    list_filter = ('owner',)
    search_fields = ('title', 'desc')
    list_editable = ('is_hot',)
    list_display_links = ('id', 'title')

    class Media:
        js = (
            'https://cdn.bootcdn.net/ajax/libs/jquery/3.7.1/jquery.js',
            ImportMapJS({
                "ckeditor5": "ckeditor5/ckeditor5.js",
                "ckeditor5/": "ckeditor5/"
            }),
            ModuleJS('ckeditor5/config.js'),
            # 'ckeditor5/ckeditor5.js',
            # 'ckeditor5/translations/zh.js'
        )


admin.site.register(Post, PostAdmin)