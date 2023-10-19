from django.contrib import admin
from .models import Post, Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id','title','username']
    list_filter=['title','username']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['body','id',]
