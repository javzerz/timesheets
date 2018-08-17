from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import ListView, DetailView
from .models import News_Article

app_name = 'news'

urlpatterns = [
    path('news/', ListView.as_view(queryset=News_Article.objects.all().order_by("-date")[:25],
     template_name="news/news.html")),
    path('news/<int:pk>/', DetailView.as_view(model=News_Article, template_name='news/article.html')),
]
