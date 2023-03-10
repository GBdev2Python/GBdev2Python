from django.urls import path
from serviceapp.apps import ServiceappConfig
from .views import *

app_name = ServiceappConfig.name

urlpatterns = [
    path('response/<int:vacancyheader>/', response, name='response'),
    path("responseview/<int:response_id>/", response_employer, name="response_view"),
    path("responseviewapplicant/<int:response_id>/", response_applicant, name="response_view_applicant"),
    # удалить вакансию
    path("response_delete/<int:response_id>/", ResponseDelete.as_view(), name="response_delete"),
    path("response_update/<int:response_id>/", ResponseUpdate.as_view(), name="response_update"),
]