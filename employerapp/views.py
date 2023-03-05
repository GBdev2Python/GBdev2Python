from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView

from authapp.models import *
from employerapp.forms import *
from employerapp.models import *
from serviceapp.models import Response


class EmployerList(ListView):
    """Список всех ваканский через employerapp"""
    model = Employer
    template_name = "employerapp/employer_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employer_lst_qs"] = Employer.objects.all()
        return context


class VacancyJob(TemplateView):
    """Описание вакансии"""
    template_name = "employerapp/vacancy.html"
    model = Employer

    def get_context_data(self, vacancy_pk, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancy_qs"] = get_object_or_404(VacancyHeader, pk=vacancy_pk)
        if self.request.user.id == VacancyHeader.objects.get(pk=vacancy_pk).employer.user.id:
            print(self.request.user.id)
            context["response"] = Response.objects.all().filter(vacancyheader=vacancy_pk)

        return context


# class DetailEmployer(TemplateView):
#     template_name = "employerapp/employer_detail.html"
#     model = Employer
#
#     def get_context_data(self, employer, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["employer_qs"] = get_object_or_404(Employer, pk=employer)
#         return context


class DetailEmployer(DetailView):
    """Detail view по работодателю"""
    model = Employer
    template_name = "employerapp/employer_detail.html"
    pk_url_kwarg = "employer"
    context_object_name = "employer_qs"


#TODO ОПРЕДЕЛИТЬСЯ НУЖНА ЛИ ЭТА ВЬЮХА?
class AllVacancyList(ListView):
    paginate_by = 5
    model = VacancyHeader
    template_name = "employerapp/vacancy_list.html"

    # Отображаем при пагинации только опубликованные вакансии
    def get_queryset(self):
        return VacancyHeader.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_vacancy_lst_qs"] = VacancyHeader.objects.all().filter(is_published=True)
        return context


class EmployerVacancyList(TemplateView):
    """Список вакансий по работодателю"""
    template_name = "employerapp/employer_vacancy_list.html"

    def get_context_data(self, vacancy_employer, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employer_vacancy_lst_qs"] = (
            VacancyHeader.objects.all().exclude(is_published=False).filter(employer_id=vacancy_employer)
        )
        context["employer_lst_qs"] = (
            VacancyHeader.objects.all().exclude(is_published=False).filter(employer_id=vacancy_employer).first()
        )
        return context


# TODO Если у юзера есть профиль работодателя - редиректить на его кабинет
class EmployerCreate(CreateView):
    """Создание профиля работодателя"""
    form_class = AddEmployerForm
    template_name = "employerapp/employer_create.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object = self.object.save()
        return super().form_valid(form)


class EmployerUpdate(UpdateView):
    model = Employer
    form_class = UpdateEmployerForm
    pk_url_kwarg = "employer"
    template_name = "employerapp/employer_update.html"


class VacancyCreate(CreateView):
    form_class = AddVacancyForm
    template_name = "employerapp/vacancy_create.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.employer_id = Employer.objects.get(user=self.request.user)
        self.object = self.object.save()
        return super().form_valid(form)


# TODO Если не владелец вакансии - не может редактировать
class VacancyUpdate(UpdateView):
    model = VacancyHeader
    form_class = UpdateVacancyForm
    pk_url_kwarg = "vacancy"
    template_name = "employerapp/vacancy_update.html"


# TODO Если не владелец вакансии - не может редактировать
class VacancyDelete(DeleteView):
    model = VacancyHeader
    pk_url_kwarg = "vacancy"
    template_name = "employerapp/vacancy_delete.html"
    success_url = reverse_lazy("hhapp:main_page")


# TODO Если не владец - Либо редирект в кабинет, либо в шаблон не выводить кнопку редактирования
class EmployerCabinet(TemplateView):
    template_name = "employerapp/employer_cabinet.html"
    pk_url_kwarg = "employer"

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

        return context
