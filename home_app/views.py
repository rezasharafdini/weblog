from django.shortcuts import render
from django.views.generic import TemplateView
from article_app import models


class HomeView(TemplateView):
    template_name = 'home_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = models.Article.objects.all()[:3]
        return context
