from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()

    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subs')
    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField()
    is_publish = models.BooleanField(default=False)

    category = models.ManyToManyField(Category, related_name='articles')

    created_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
