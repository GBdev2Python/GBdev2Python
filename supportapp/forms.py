from django import forms

from .models import Ticket, TicketMessage


class CreateTicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['user', 'topic', 'init_message']
        widgets = {
            'user': forms.HiddenInput()
        }


class CreateTicketMessageForm(forms.ModelForm):

    def __init__(self, *args, user=None, ticket=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and ticket:
            self.fields["user"].initial = user.id
            self.fields["ticket"].initial = ticket.id

    class Meta:
        model = TicketMessage
        fields = ("user", "ticket", "message")
        widgets = {
            'user': forms.HiddenInput,
            'ticket': forms.HiddenInput,
        }


class TicketChangeStatusForm(forms.ModelForm):

    def __init__(self, *args, user=None, ticket=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and ticket:
            self.fields["user"].initial = user.id

    class Meta:
        model = Ticket
        fields = ("user", "status")
        widgets = {
            "user": forms.HiddenInput,
            "status": forms.HiddenInput,
        }
