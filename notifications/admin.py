from django.contrib import admin
from .models import *


@admin.register(Notification)
class PostsAdmin(admin.ModelAdmin):
    fields = ['user', 'type']

