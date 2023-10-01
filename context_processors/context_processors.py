from article_app import models


def all_category(request):
    all_categories = models.Category.objects.order_by('-created_at').filter(is_publish=True)
    return {'all_categories': all_categories}


def recent_article(request):
    recent_article = models.Article.objects.order_by('-update').filter(is_publish=True)[:3]
    return {'recent_article': recent_article}


def first_article(request):
    first_article = models.Article.objects.filter(is_publish=True).first()
    return {'first_article': first_article}
