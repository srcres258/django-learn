from django.contrib import admin

# Register your models here.
from .models import Category, Post, Tag, Sidebar

for model in [Category, Post, Tag, Sidebar]:
    admin.site.register(model)