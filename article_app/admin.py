from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_publish')
    list_filter = ('is_publish',)
    search_fields = ('name', 'slug')
    list_editable = ('is_publish',)


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_publish')
    list_filter = ('is_publish',)
    search_fields = ('title', 'slug')
    list_editable = ('is_publish',)
