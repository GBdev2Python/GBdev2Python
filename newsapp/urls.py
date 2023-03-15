from django.urls import path

from newsapp.apps import NewsappConfig

from .views import NewsDetailView, NewsListView

app_name = NewsappConfig.name

urlpatterns = [
    path("", NewsListView.as_view(), name="news"),
    path("<int:pk>/detail", NewsDetailView.as_view(), name="news_detail"),
]
