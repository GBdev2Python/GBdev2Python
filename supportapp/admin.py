from django.contrib import admin

from .models import Ticket, TicketMessage


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    pass
