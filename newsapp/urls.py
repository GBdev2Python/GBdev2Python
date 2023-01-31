from django.urls import path

from .views import NewsListView, NewsDetailView
from newsapp.apps import NewsappConfig


app_name = NewsappConfig.name

urlpatterns = [
    path('', NewsListView.as_view(), name='news'),
    path('<int:pk>/detail', NewsDetailView.as_view(), name='news_detail'),
]
