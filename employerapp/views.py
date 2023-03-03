from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView

from authapp.models import *
from employerapp.forms import *
from employerapp.models import *
from serviceapp.models import Response


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
        if self.request.user.id == VacancyHeader.objects.get(pk=vacancy_pk).employer.user.id:
            print(self.request.user.id)
            context["response"]= Response.objects.all().filter(vacancyheader=vacancy_pk)

        # context["vacancy_body_qs"] = VacancyBody.objects.all().filter(vacancy_header_id=vacancy_pk)
        return context


# Карточка работодателя
# class DetailEmployer(TemplateView):
#     template_name = "employerapp/employer_detail.html"
#     model = Employer
#
#     def get_context_data(self, employer, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["employer_qs"] = get_object_or_404(Employer, pk=employer)
#         return context

# Карточка работодателя
class DetailEmployer(DetailView):
    model = Employer
    template_name = "employerapp/employer_detail.html"
    pk_url_kwarg = "employer"
    context_object_name = "employer_qs"


# Список всех вакансий сайта
class AllVacancyList(ListView):
    paginate_by = 8
    model = VacancyHeader
    template_name = "employerapp/vacancy_list.html"
    # template_name = "hhapp/jobs.html"

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
            VacancyHeader.objects.all().exclude(is_published=False).filter(employer=vacancy_employer_pk)
        )
        context["employer_lst_qs"] = (
            VacancyHeader.objects.all().exclude(is_published=False).filter(employer=vacancy_employer_pk).first()
        )
        return context


# Создание карточки работодателя
class EmployerCreate(CreateView):
    form_class = AddEmployerForm
    template_name = "employerapp/employer_create.html"
    # success_url = reverse_lazy("employerapp:employer_list")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.user=self.request.user
        self.object = self.object.save()
        return super().form_valid(form)


# Изменение карточки работодателя
class EmployerUpdate(UpdateView):
    model = Employer
    form_class = UpdateEmployerForm
    pk_url_kwarg = "employer"
    template_name = "employerapp/employer_update.html"
    # success_url = reverse_lazy("employerapp:employer_detail")


# Создание вакансии работодателя
class VacancyCreate(CreateView):
    form_class = AddVacancyForm
    template_name = "employerapp/vacancy_create.html"
    # success_url = reverse_lazy("employerapp:employer_list")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.employer=Employer.objects.get(user=self.request.user)
        self.object = self.object.save()
        return super().form_valid(form)



# Изменение вакансии работодателя
class VacancyUpdate(UpdateView):
    model = VacancyHeader
    form_class = UpdateVacancyForm
    pk_url_kwarg = "vacancy_id"
    template_name = "employerapp/vacancy_update.html"
    # success_url = reverse_lazy("employerapp:employer_detail")


# Удаление вакансии
class VacancyDelete(DeleteView):
    model = VacancyHeader
    pk_url_kwarg = "vacancy_id"
    template_name = "employerapp/vacancy_delete.html"
    success_url = reverse_lazy("hhapp:main_page")
    # success_url = reverse_lazy("employerapp:employer_detail", kwargs={'employer': 3})


#  * * * * * * * * * * * * * * * * * * * *    В разработке   * * * * * * * * * * * * * * * * * * * *
# Домашний кабинет работодателя
# http://127.0.0.1:8000/employerapp/employer_cabinet/1/


class EmployerCabinet(TemplateView):
    template_name = "employerapp/employer_cabinet.html"
    pk_url_kwarg = "employer"
    # query_pk_and_slug = False  get_object_or_404(Employer, pk=employer)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Компания залогиненного работодателя
        context["employer_cab_comp_qs"] = Employer.objects.filter(id=self.kwargs["employer"])

        # Проверка создания карточки работодателя
        context["employer_cab_cnt_qs"] = Employer.objects.filter(pk=self.kwargs["employer"]).count()

        # Выборка всех публикованных вакансий работодателя
        emp = Employer.objects.get(id=self.kwargs["employer"])
        context["vacancy_cab_qs"] = VacancyHeader.objects.filter(employer_id__employment=emp, is_published=True)

        # Выборка НЕопубликованных вакансий работодателя
        context["vacancy_cab_not_qs"] = VacancyHeader.objects.filter(employer_id__employment=emp, is_published=False)


        # Открытие созданной карточки работодателя на редактирование

        return context
