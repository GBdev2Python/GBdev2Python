from django.urls import path

# from employerapp import views
from employerapp.apps import EmployerappConfig
from employerapp.views import *

app_name = EmployerappConfig.name

# http://127.0.0.1:8000/admin/login/?next=/admin/

urlpatterns = [
    # список всех работодателей
    path("employer_list/", EmployerList.as_view(), name="employer_list"),
    # http://127.0.0.1:8000/employerapp/employer_list/
    # Карточка работодателя
    path("employer_detail/<slug:employer_slug>/", DetailEmployer.as_view(), name="employer_detail"),
    # Список всех вакансий сайта
    path("vacancy_list/", AllVacancyList.as_view(), name="vacancy_list"),
    # http://127.0.0.1:8000/employerapp/vacancy_list/
    # Список вакансий работодателя
    path(
        "employer_vacancy_list/<int:vacancy_employer_pk>/", EmployerVacancyList.as_view(), name="employer_vacancy_list"
    ),
    # отдельная вакансия
    path("vacancy/<int:vacancy_pk>/", VacancyJob.as_view(), name="vacancy"),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    # Создание карточки работодателя
    path("employer_create/", EmployerCreate.as_view(), name="employer_create"),
    # http://127.0.0.1:8000/employerapp/employer_create/
    # Создание карточки работодателя
    path("vacancy_create/", VacancyCreate.as_view(), name="vacancy_create"),
    # http://127.0.0.1:8000/employerapp/vacancy_create/
    # Редактирование карточки работодателя
    path("employer_update/<slug:employer_slug>/", EmployerUpdate.as_view(), name="employer_update"),
    # http://127.0.0.1:8000/employerapp/employer_update/allegrova-irina-aleksandrovna/
    path("employer_cabinet/<slug:employer_slug>/", EmployerCabinet.as_view(), name="employer_cabinet"),
    # http://127.0.0.1:8000/employerapp/employer_cabinet/allegrova-irina-aleksandrovna/
]
