from django.urls import path

from employerapp.apps import EmployerappConfig
from employerapp.views import *

app_name = EmployerappConfig.name

urlpatterns = [
    # Карточка работодателя на сайте http://127.0.0.1:8000/employerapp/employer_detail/5/
    path("employer_detail/<int:employer>/", DetailEmployer.as_view(), name="employer_detail"),
    # отдельная вакансия сайта  http://127.0.0.1:8000/employerapp/vacancy/2/
    path("vacancy/<int:vacancy_pk>/", VacancyJob.as_view(), name="vacancy"),
    # Создание карточки работодателя   http://127.0.0.1:8000/employerapp/employer_create/
    path("employer_create/", EmployerCreate.as_view(), name="employer_create"),
    # Редактирование карточки работодателя   http://127.0.0.1:8000/employerapp/employer_update/5/
    path("employer_update/<int:employer>/", EmployerUpdate.as_view(), name="employer_update"),
    # Создание вакансии работодателя (конкретный пользователь)  http://127.0.0.1:8000/employerapp/vacancy_create/
    path("vacancy_create/", VacancyCreate.as_view(), name="vacancy_create"),
    # Редактирование вакансии работодателя   http://127.0.0.1:8000/employerapp/vacancy_update/2/
    path("vacancy_update/<int:vacancy>/", VacancyUpdate.as_view(), name="vacancy_update"),
    # удалить вакансию   http://127.0.0.1:8000/employerapp/vacancy_delete/7/
    path("vacancy_delete/<int:vacancy>/", VacancyDelete.as_view(), name="vacancy_delete"),
    # Кабинет работодателя (конкретный пользователь)  http://127.0.0.1:8000/employerapp/employer_cabinet/5/
    path("employer_cabinet/<int:employer>/", EmployerCabinet.as_view(), name="employer_cabinet"),
    # Список вакансий работодателя на сайте  http://127.0.0.1:8000/employerapp/employer_vacancy_list/5/
    path(
        "employer_vacancy_list/<int:vacancy_employer>/", EmployerVacancyList.as_view(), name="employer_vacancy_list"
    ),

    # Нижерасположенные роуты рабочие, но в приложении не используются.
    # Список всех работодателей сайта  http://127.0.0.1:8000/employerapp/employer_list/
    path("employer_list/", EmployerList.as_view(), name="employer_list"),
    # Список всех вакансий сайта  http://127.0.0.1:8000/employerapp/vacancy_list/
    path("vacancy_list/", AllVacancyList.as_view(), name="vacancy_list"),
]
