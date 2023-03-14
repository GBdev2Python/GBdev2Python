from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView
from django.db.models import Prefetch, Count
from .filter import VacancyFilter, ResumeFilter

from .forms import FeedbackMailForm
from newsapp.models import News
from employerapp.models import Employer, VacancyHeader
from applicantapp.models import Resumes
from django.conf import settings


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
    # paginate_by = 5  # Прибавляются дубли из context['filter']
    model = VacancyHeader
    template_name = "hhapp/jobs.html"

    # Отображаем при пагинации только опубликованные вакансии
    def get_queryset(self):
        return VacancyHeader.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_vacancy_lst_qs"] = VacancyHeader.objects.filter(is_published=True)
        # context["employer_lst_qs"] = Employer.objects.all()
        context['filter'] = VacancyFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CandidateListView(ListView):
    model = Resumes
    template_name = "hhapp/candidate.html"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_resume_lst_qs"] = Resumes.objects.all().filter(is_published=True)
        context['filter'] = ResumeFilter(self.request.GET, queryset=self.get_queryset())
        return context


class SiteNavigationView(TemplateView):
    template_name = 'hhapp/navigation.html'


class ContactUsView(FormView):
    """
    Вьюха формы отправки письма пользователя из тех поддержки.
    Успешный редирект - на просмотр письма
    TODO: Добавить таймаут на отправку письма в поддержку через кэш
    """
    template_name = 'hhapp/contact_us.html'
    form_class = FeedbackMailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            feedback_form = FeedbackMailForm(
                user=self.request.user
            )
            context['feedback_form'] = feedback_form
            context['admin_mail'] = settings.TECH_SUPPORT_EMAIL
        return context

    def form_valid(self, form):
        send_mail(
            subject=form.cleaned_data['topic'],
            message=form.cleaned_data['message'],
            from_email=self.request.user.email,
            recipient_list=[settings.TECH_SUPPORT_EMAIL, ],
            fail_silently=False,
        )
        return HttpResponseRedirect(reverse_lazy('hhapp:support_success'))

    def form_invalid(self, form):
        context = self.get_context_data()
        context.update({'feedback_form': form})
        return render(self.request, template_name=self.template_name, context=context)


class SupportMailSuccessView(TemplateView):
    template_name = 'hhapp/support_mail_success.html'
