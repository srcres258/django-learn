from django.contrib import admin

# Register your models here.
from .models import Category, Post, Tag

for model in [Category, Post, Tag]:
    admin.site.register(model)