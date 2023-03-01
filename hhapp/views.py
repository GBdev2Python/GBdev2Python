from django.views.generic import TemplateView, ListView
from django.db.models import Prefetch, Count
from .filter import VacancyFilter

from newsapp.models import News
from employerapp.models import Employer, VacancyHeader
from applicantapp.models import Resumes, Applicants


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
    queryset = VacancyHeader.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_vacancy_lst_qs"] = VacancyHeader.objects.all().filter(is_published=True)
        # context["employer_lst_qs"] = Employer.objects.all()
        context['filter'] = VacancyFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CandidateListView(ListView):
    model = Resumes

    template_name = "hhapp/candidate.html"
    paginate_by = 9

    def get_queryset(self):

        if self.request.user.is_authenticated:
            curent_applicant = Applicants.objects.filter(user=self.request.user)
            obj = Resumes.objects.exclude(applicants__in=curent_applicant)
        else:
            obj = Resumes.objects.all()
        return obj.filter(is_published=True)


   # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
     #   curent_applicant = Applicants.objects.filter(user=self.request.user)
      #  queryset = Resumes.objects.filter(is_published=1)
       # print (queryset)
        #context["resumes"] = Resumes.objects.filter(applicants=self.kwargs["applicant_id"])
      #  context["queryset"] =queryset
      #  return context
