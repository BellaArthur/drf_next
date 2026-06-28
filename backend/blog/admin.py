from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display   = ['title', 'author', 'category', 'status', 'created_at']
    list_filter    = ['status', 'category']
    search_fields  = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal   = ['tags']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ['author', 'post', 'created_at']
    search_fields = ['body', 'author__email']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']