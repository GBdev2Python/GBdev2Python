from django.views.generic import TemplateView
from django.db.models import Prefetch, Count

from newsapp.models import News
from employerapp.models import Employer, VacancyHeader


class MainPageView(TemplateView):
    template_name = "hhapp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO Тут должно быть кеширование, или извлечение данных с кэша
        context["news_objects"] = News.objects.all()[:5]
        context["employer_objects"] = Employer.objects.all().annotate(
            company_vacancies=Count('vacancies__id'),
        ).only('employment')[:7]

        return context


class JobsListView(TemplateView):
    template_name = "hhapp/jobs.html"


class CandidateListView(TemplateView):
    template_name = "hhapp/candidate.html"
