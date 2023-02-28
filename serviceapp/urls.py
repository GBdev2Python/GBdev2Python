from django.urls import path
from serviceapp.apps import ServiceappConfig
from .views import *

app_name = ServiceappConfig.name

urlpatterns = [
    path('response/<int:vacancyheader>/', response, name='response'),
    path("responseview/<int:response_id>/", response_view, name="response_view"),
]