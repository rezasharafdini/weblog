from django.db import models
from django.utils.html import format_html
from account_app.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()
    image = models.ImageField(upload_to='category/image')

    parent = models.ForeignKey('self', null=True,blank=True,on_delete=models.CASCADE, related_name='subs')
    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="50px" height="50px">')

    show_image.short_description = 'image'


class Article(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField()

    is_publish = models.BooleanField(default=False)

    category = models.ManyToManyField(Category, related_name='articles')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article')

    image = models.ImageField(upload_to='article/image')

    created_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="50px" height="50px">')

    show_image.short_description = 'image'
