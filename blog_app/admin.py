from django.contrib import admin

from .models import PostCategory, Post, PostComment

# Register your models here.
admin.site.register(PostCategory)
admin.site.register(Post)
admin.site.register(PostComment)