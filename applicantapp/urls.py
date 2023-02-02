from django.urls import path
from applicantapp import views

urlpatterns = [
    # список Соискателей
    path('applicant_list/', views.ApplicantList.as_view(),name='applicant_list'),
    # список Резюме
    path('resume_list/', views.ResumeList.as_view(),name='resume_list'),
    # отдельное Резюме
    path('resume/<str:resume_id>/', views.Resume.as_view(),name='resume_by_id'),
    # отдельный Соискатель
    path('applicant/<str:applicant_id>/', views.Applicant.as_view(),name='applicant_by_id'),

]