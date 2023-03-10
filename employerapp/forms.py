from ckeditor.widgets import CKEditorWidget
from django import forms
from employerapp.models import *


class AddEmployerForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget, label="Детальное описание")

    class Meta:
        model = Employer
        fields = ["employment", "cover", "town", "address", "phone", "email", "website", "body", "location"]
        labels = {
            "employment": "Название организации",
            "town": "Город (населенный пункт)",
            "location": "Место расположения организации на карте",
        }
        widgets = {
            "employment": forms.Textarea(attrs={"cols": 50, "rows": 3}),
            "address": forms.Textarea(attrs={"cols": 50, "rows": 3}),
            "body": forms.CharField(widget=CKEditorWidget()),
            "location": forms.Textarea(attrs={"cols": 100, "rows": 10}),
        }


class UpdateEmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ["employment", "cover", "town", "address", "phone", "email", "website", "body", "location"]

        labels = {
            "employment": "Название организации",
            "town": "Расположение организации",
            "location": "Место расположения организации на карте",
        }
        widgets = {
            "employment": forms.Textarea(attrs={"cols": 50, "rows": 3}),
            "address": forms.Textarea(attrs={"cols": 50, "rows": 3}),
            "location": forms.Textarea(attrs={"cols": 100, "rows": 10}),
        }

        help_texts = {
            "phone": "Введите номер в формате +71234567890",
        }


class AddVacancyForm(forms.ModelForm):

    class Meta:
        model = VacancyHeader
        fields = [
            "job_title",
            "salary",
            "experience",
            "employment",
            "town",
            "skills",
            "body",
           # "employer",
            "is_published",
        ]
        widgets = {
            # "skills": forms.CheckboxSelectMultiple(),
            "skills": forms.SelectMultiple(),
            # "employer": forms.HiddenInput(),
        }


class UpdateVacancyForm(forms.ModelForm):
    class Meta:
        model = VacancyHeader
        fields = [
            "job_title",
            "salary",
            "experience",
            "employment",
            "town",
            "skills",
            "body",
            # "employer",
            "is_published",
        ]
        widgets = {
            # "skills": forms.CheckboxSelectMultiple(),
            "skills": forms.SelectMultiple(),
            "employer": forms.HiddenInput(),
        }
