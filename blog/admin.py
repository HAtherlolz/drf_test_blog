from django.contrib import admin
from .models import *


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    fields = ['user', 'title', 'text']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ['user', 'post', 'comment_text']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'password', 'is_active']


@admin.register(UserFollowing)
class UserFollowinAdmin(admin.ModelAdmin):
    fields = ['user_id', 'following_user_id']