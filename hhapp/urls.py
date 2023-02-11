from django.urls import path

from hhapp import views
from hhapp.apps import HhappConfig

app_name = HhappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),
    path("jobs/", views.JobsListView.as_view(), name="jobs"),
    path("candidate/", views.CandidateListView.as_view(), name="candidate"),
]
