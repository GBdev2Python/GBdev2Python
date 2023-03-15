from django import forms
from .models import Response
import re

class ResponseForm(forms.ModelForm):
    cover_letter = forms.CharField(label='Сопроводительное письмо',widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Response
        fields = ["cover_letter"]

class ResponseChangeStatusForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ["status"]


class UpdateResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ["cover_letter"]

        labels = {
            "cover_letter": "Сопроводительное письмо",
        }
        widgets = {
            "cover_letter": forms.Textarea(attrs={'class': 'form-control'}),
        }
