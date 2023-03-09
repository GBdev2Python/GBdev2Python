from django.urls import path

from .apps import SupportappConfig
from .views import TicketsListView, TicketCreationView, CreateTicketMessageView, TicketDetailView, TicketChangeStatusView


app_name = SupportappConfig.name

urlpatterns = [
    path('tickets/', TicketsListView.as_view(), name='tickets'),
    path('create_ticket/', TicketCreationView.as_view(), name='create_ticket'),
    path('ticket/<int:pk>', TicketDetailView.as_view(), name='ticket'),
    path('create_message/', CreateTicketMessageView.as_view(), name='create_message'),
    path('change_status/<int:pk>', TicketChangeStatusView.as_view(), name='status_change'),
]
