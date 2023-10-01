from django.shortcuts import render
from django.views.generic import DetailView, ListView
from . import models


class ArticleDetailView(DetailView):
    model = models.Article
    queryset = models.Article.objects.filter(is_publish=True)


class ArticleListView(ListView):
    model = models.Article
    queryset = models.Article.objects.filter(is_publish=True)
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        category = self.request.GET.get('category')
        if search:
            queryset = queryset.filter(title__icontains=search)

        if category:
            queryset = queryset.filter(category__name=category)
        return queryset
