from django.urls import path

from hhapp import views
from hhapp.apps import HhappConfig

app_name = HhappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),
]
