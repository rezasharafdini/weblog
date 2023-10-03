from django.urls import path
from . import views

app_name = 'article_app'
urlpatterns = [
    path('detail/<str:slug>/', views.ArticleDetailView.as_view(), name='detail'),
    path('list/', views.ArticleListView.as_view(), name='list'),
    path('add/comment', views.AddCommentView.as_view(), name='add_comment')
]
