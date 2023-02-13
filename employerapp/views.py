from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView
from authapp.models import *

from employerapp.forms import *
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
# class VacancyJob(TemplateView):
class VacancyJob(TemplateView):
    template_name = "employerapp/vacancy.html"
    model = Employer

    def get_context_data(self, vacancy_pk, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancy_qs"] = get_object_or_404(VacancyHeader, pk=vacancy_pk)
        # context["vacancy_body_qs"] = VacancyBody.objects.all().filter(vacancy_header_id=vacancy_pk)
        return context


# Карточка работодателя
# class DetailEmployer(TemplateView):
#     template_name = "employerapp/employer_detail.html"
#     model = Employer
#
#     def get_context_data(self, employer_id, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["employer_qs"] = get_object_or_404(Employer, pk=employer_id)
#         return context

# Карточка работодателя
class DetailEmployer(DetailView):
    model = Employer
    template_name = "employerapp/employer_detail.html"
    pk_url_kwarg = "employer_id"
    context_object_name = "employer_qs"


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
        context["employer_vacancy_lst_qs"] = (
            VacancyHeader.objects.all().exclude(is_published=False).filter(employer_id=vacancy_employer_pk)
        )
        context["employer_lst_qs"] = (
            VacancyHeader.objects.all().exclude(is_published=False).filter(employer_id=vacancy_employer_pk).first()
        )
        return context


# Создание карточки работодателя
class EmployerCreate(CreateView):
    form_class = AddEmployerForm
    template_name = "employerapp/employer_create.html"
    # success_url = reverse_lazy("employerapp:employer_list")


# Изменение карточки работодателя
class EmployerUpdate(UpdateView):
    model = Employer
    form_class = UpdateEmployerForm
    pk_url_kwarg = "employer_id"
    template_name = "employerapp/employer_update.html"
    # success_url = reverse_lazy("employerapp:employer_detail")



# Создание вакансии работодателя
class VacancyCreate(CreateView):
    form_class = AddVacancyForm
    template_name = "employerapp/vacancy_create.html"
    # success_url = reverse_lazy("employerapp:employer_list")


# Изменение карточки работодателя
class VacancyUpdate(UpdateView):
    model = VacancyHeader
    form_class = UpdateVacancyForm
    pk_url_kwarg = "vacancy_id"
    template_name = "employerapp/vacancy_update.html"
    # success_url = reverse_lazy("employerapp:employer_detail")


#  * * * * * * * * * * * * * * * * * * * *    В разработке   * * * * * * * * * * * * * * * * * * * *
# Домашний кабинет работодателя
# http://127.0.0.1:8000/employerapp/employer_cabinet/1/

class EmployerCabinet(TemplateView):
    template_name = "employerapp/employer_cabinet.html"
    pk_url_kwarg = "employer_id"
    # query_pk_and_slug = False  get_object_or_404(Employer, pk=employer_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Компания залогиненного работодателя
        context["employer_cab_qs"] = Employer.objects.filter(pk=self.kwargs["employer_id"])

        # Проверка создания карточки работодателя
        context["employer_cab_cnt_qs"] = Employer.objects.filter(pk=self.kwargs["employer_id"]).count()

        # Выборка всех вакансий работодателя (залогиненный пользователь)
        context["vacancy_cab_qs"] = VacancyHeader.objects.filter(employer_id=self.kwargs["employer_id"])

        # Открытие созданной карточки работодателя на редактирование


        return context
