from django.views.generic import TemplateView, ListView
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


class JobsListView(ListView):
    model = VacancyHeader
    template_name = "hhapp/jobs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_vacancy_lst_qs"] = VacancyHeader.objects.all().filter(is_published=True)
        # context["employer_lst_qs"] = Employer.objects.all()
        return context


class CandidateListView(TemplateView):
    template_name = "hhapp/candidate.html"
