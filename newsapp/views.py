from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import News


class NewsListView(ListView):
    model = News
    paginate_by = 10
    template_name = "news/news_list_view.html"

    # TODO: add filter functionality
    def get_queryset(self):
        return super().get_queryset()


class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_detail_view.html"

