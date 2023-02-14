from django.views.generic import TemplateView

# Create your views here.


class MainPageView(TemplateView):
    template_name = "hhapp/index.html"

    def get_context_data(self, **kwargs):
        # Get all previous data
        context = super().get_context_data(**kwargs)
        # Create your own data
        context["news_title"] = "Громкий новостной заголовок"
        context[
            "news_preview"
        ] = "Предварительное описание, которое заинтересует каждого"
        context["range"] = range(5)
        return context


class JobsListView(TemplateView):
    template_name = "hhapp/jobs.html"


class CandidateListView(TemplateView):
    template_name = "hhapp/candidate.html"
