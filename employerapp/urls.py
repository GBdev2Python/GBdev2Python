from django.urls import path

from employerapp.apps import EmployerappConfig
from employerapp.views import *

app_name = EmployerappConfig.name


urlpatterns = [
    # список всех работодателей сайта
    path("employer_list/", EmployerList.as_view(), name="employer_list"),
    # http://127.0.0.1:8000/employerapp/employer_list/
    # Карточка работодателя на сайте
    path("employer_detail/<int:employer>/", DetailEmployer.as_view(), name="employer_detail"),
    # http://127.0.0.1:8000/employerapp/employer_detail/5/
    # Список всех вакансий сайта
    path("vacancy_list/", AllVacancyList.as_view(), name="vacancy_list"),
    # http://127.0.0.1:8000/employerapp/vacancy_list/
    # отдельная вакансия сайта
    path("vacancy/<int:vacancy_pk>/", VacancyJob.as_view(), name="vacancy"),
    # http://127.0.0.1:8000/employerapp/vacancy/2/
    # Список вакансий работодателя на сайте
    path(
        "employer_vacancy_list/<int:vacancy_employer>/", EmployerVacancyList.as_view(), name="employer_vacancy_list"
    ),
    # http://127.0.0.1:8000/employerapp/employer_vacancy_list/5/
    # Создание карточки работодателя (конкретный пользователь)
    path("employer_create/", EmployerCreate.as_view(), name="employer_create"),
    # http://127.0.0.1:8000/employerapp/employer_create/

    # Редактирование карточки работодателя (конкретный пользователь)
    path("employer_update/<int:employer>/", EmployerUpdate.as_view(), name="employer_update"),
    # http://127.0.0.1:8000/employerapp/employer_update/5/
    # Создание вакансии работодателя (конкретный пользователь)
    path("vacancy_create/", VacancyCreate.as_view(), name="vacancy_create"),
    # http://127.0.0.1:8000/employerapp/vacancy_create/
    # Редактирование вакансии работодателя (конкретный пользователь)
    path("vacancy_update/<int:vacancy>/", VacancyUpdate.as_view(), name="vacancy_update"),
    # http://127.0.0.1:8000/employerapp/vacancy_update/2/

    # удалить вакансию
    path("vacancy_delete/<int:vacancy>/", VacancyDelete.as_view(), name="vacancy_delete"),
    # http://127.0.0.1:8000/employerapp/vacancy_delete/7/

    # Кабинет работодателя (конкретный пользователь)
    path("employer_cabinet/<int:employer>/", EmployerCabinet.as_view(), name="employer_cabinet"),
    # http://127.0.0.1:8000/employerapp/employer_cabinet/5/
]
