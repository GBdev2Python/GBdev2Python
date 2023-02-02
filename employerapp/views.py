from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView
from employerapp.models import *


class MainPageView(TemplateView):
    template_name = "employerapp/home.html"


# Список всех работодателей
class EmployerList(ListView):
    model = Employer
    template_name = "employerapp/employer_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employer_lst_qs"] = Employer.objects.all()
        return context


# Вакансия работодателя (выбранная)
class VacancyJob(TemplateView):
    template_name = "employerapp/vacancy.html"

    def get_context_data(self, vacancy_pk, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancy_qs"] = get_object_or_404(VacancyHeader, pk=vacancy_pk)
        context["vacancy_body_qs"] = VacancyBody.objects.all().filter(vacancy_header_id=vacancy_pk)
        return context


# Карточка работодателя
class DetailEmployer(TemplateView):
    template_name = "employerapp/employer_detail.html"

    def get_context_data(self, employer_slug, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employer_qs"] = get_object_or_404(Employer, slug=employer_slug)
        return context


# Список всех вакансий сайта
class AllVacancyList(ListView):
    model = VacancyHeader
    template_name = "employerapp/vacancy_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_vacancy_lst_qs"] = VacancyHeader.objects.all().filter(is_published=True)
        return context


# Список вакансий работодателя
class EmployerVacancyList(TemplateView):
    template_name = "employerapp/employer_vacancy_list.html"

    def get_context_data(self, vacancy_employer_pk, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employer_vacancy_lst_qs"] = VacancyHeader.objects.all().exclude(is_published=False).filter(
            employer_id=vacancy_employer_pk)
        context["employer_lst_qs"] = VacancyHeader.objects.all().exclude(is_published=False).filter(
            employer_id=vacancy_employer_pk).first()
        return context