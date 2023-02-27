from django import forms
from .models import Response
import re

class ResponseForm(forms.ModelForm):
    cover_letter = forms.CharField(label='Сопроводительное письмо',widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Response
        fields = ["cover_letter"]