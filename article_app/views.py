from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic import DetailView, ListView
from . import models
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin


class ArticleDetailView(DetailView):
    model = models.Article
    queryset = models.Article.objects.filter(is_publish=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.AddCommentForm()
        return context


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


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request):
        parent_id = self.request.POST.get('parent_id')
        article_id = self.request.POST.get('article_id')
        article = models.Article.objects.get(id=int(article_id))
        form = forms.AddCommentForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            comment = models.Comment.objects.create(user=self.request.user, article=article, parent_id=parent_id,
                                                    subject=cd['subject'], content=cd['content'])
            number_comments = models.Comment.objects.filter(user=self.request.user, article=article).all().count()
            if not parent_id:
                return JsonResponse(
                    {'Reply': 'False', 'ImageUrl': request.user.image.url, 'FullName': request.user.full_name,
                     'CreatedAt': comment.created_at, 'Content': comment.content, 'CommentId': comment.id,
                     'NumberComments': number_comments})

            return JsonResponse(
                {'Reply': 'True', 'ImageUrl': request.user.image.url, 'FullName': request.user.full_name,
                 'CreatedAt': comment.created_at, 'Content': comment.content,
                 'ParentId': parent_id, 'NumberComments': number_comments})
