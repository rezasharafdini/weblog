from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_publish', 'show_image')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_publish',)
    search_fields = ('name', 'slug')
    list_editable = ('is_publish',)


class CommentAdmin(admin.StackedInline):
    model = models.Comment

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_publish', 'show_image')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_publish',)
    search_fields = ('title', 'slug')
    list_editable = ('is_publish',)
    inlines = (CommentAdmin,)


admin.site.register(models.Comment)