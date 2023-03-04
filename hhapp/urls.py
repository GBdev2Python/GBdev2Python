from django.urls import path

from hhapp import views
from hhapp.apps import HhappConfig

app_name = HhappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),
    path("jobs/", views.JobsListView.as_view(), name="jobs"),
    path("candidate/", views.CandidateListView.as_view(), name="candidate"),
    path('navigation/', views.SiteNavigationView.as_view(), name='navigation'),
    path('contact_us', views.ContactUsView.as_view(), name='contact_us'),
    path('support_mail_success', views.SupportMailSuccessView.as_view(), name='support_success')
]
