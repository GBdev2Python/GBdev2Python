from django.views.generic import TemplateView

# Create your views here.


class MainPageView(TemplateView):
    template_name = "hhapp/index.html"

class JobsListView(TemplateView):
    template_name = "hhapp/jobs.html"

class CandidateListView(TemplateView):
    template_name = "hhapp/candidate.html"