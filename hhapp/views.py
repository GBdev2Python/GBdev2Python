from django.views.generic import TemplateView

# Create your views here.


class MainPageView(TemplateView):
    template_name = "hhapp/home.html"
