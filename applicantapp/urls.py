from django.urls import path
from applicantapp import views

urlpatterns = [
    # список Соискателей
    path('applicant_list/', views.ApplicantList.as_view(),name='applicant_list'),
    # список Резюме
    path('resume_list/', views.ResumeList.as_view(),name='resume_list'),
]
