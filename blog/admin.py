from django.contrib import admin
from .models import Tag, Category, Post

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', "author", 'category', 'created_at', 'like_count')
    list_filter = ('created_at', 'category', 'tags', 'author')
    search_fields = ('title', 'text', 'author__username', 'category__name')
    filter_horizontal=('tags', 'likes')
