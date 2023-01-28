
from django.urls import path, include
from hhapp.views import *
from django.urls import path

from hhapp import views
from hhapp.apps import HhappConfig

app_name = HhappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),

    # список всех работодателей
    path('employer_list/', EmployerList.as_view(), name="employer_list"),  # http://127.0.0.1:8000/hhapp/employer_list/
    # Карточка работодателя
    path('employer_detail/<slug:employer_slug>/', DetailEmployer.as_view(), name="employer_detail"),
    # Список всех вакансий сайта
    path('vacancy_list/', AllVacancyList.as_view(), name="vacancy_list"),  # http://127.0.0.1:8000/hhapp/vacancy_list/
    # Список вакансий работодателя
    path('employer_vacancy_list/<int:vacancy_employer_pk>/', EmployerVacancyList.as_view(), name="employer_vacancy_list"),
    # отдельная вакансия
    path('vacancy/<int:vacancy_pk>/', VacancyJob.as_view(), name="vacancy"),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    ]
