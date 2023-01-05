from django.contrib import admin
from .models import Category, Todo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name']


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'created', 'complete']
    list_display_links = ['id', 'title']
    list_editable = ['category', 'complete']
    search_fields = ['id', 'title', 'category']
