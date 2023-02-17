from django.urls import path

from applicantapp import views
from applicantapp.apps import ApplicantappConfig


app_name = ApplicantappConfig.name

urlpatterns = [
    # список Соискателей
    path("applicant_list/", views.ApplicantList.as_view(), name="list"),
    # список Резюме
    path("resume_list/", views.ResumeList.as_view(), name="resume_list"),
    # отдельное Резюме для просмотра работодателями
    path("resume/<int:resume_id>/", views.Resume.as_view(), name="resume_by_id"),
    # отдельное Резюме для просмотра соискателем
    path("applicant_resume/<int:resume_id>/", views.ApplicantResume.as_view(), name="applicant_resume"),
    # отдельный Соискатель
    path("applicant/<int:applicant_id>/", views.Applicant.as_view(), name="applicant_by_id"),
    # создание резюме
    path("new_resume/<int:applicant_id>/", views.new_resume, name="new_resume"),
    # удаление резюме
    path("delete_resume/<str:pk>/", views.delete_resume, name="delete_resume"),
    # редактирование резюме пользователя
    path("update_resume/<str:pk>/", views.update_resume, name="update_resume"),
    # заполнение профиля соискателя
    path("applicant_create/", views.ApplicantCreate.as_view(), name="create"), #пока только через строку http://127.0.0.1:8000/applicantapp/applicant_create/

    path("applicant_cabinet/<int:applicant_id>/", views.ApplicantCabinet.as_view(), name="applicant_cabinet"),

]
