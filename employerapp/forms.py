from ckeditor.widgets import CKEditorWidget
from django import forms

from employerapp.models import *


class AddEmployerForm(forms.ModelForm):

    body = forms.CharField(widget=CKEditorWidget, label="Детальное описание")

    class Meta:
        model = Employer
        fields = ["employment", "town_id", "address", "phone", "email", "website", "body", "location", "user"]
        labels = {
            "employment": "Название организации",
            "town_id": "Город (населенный пункт)",
            "location": "Место расположения организации на карте",
            # "body": "Детальное описание"
        }
        widgets = {
            "employment": forms.Textarea(attrs={"cols": 50, "rows": 3}),
            "address": forms.Textarea(attrs={"cols": 50, "rows": 3}),
            "body": forms.CharField(widget=CKEditorWidget()),
            "location": forms.Textarea(attrs={"cols": 100, "rows": 10}),
        }

    #
    #     help_texts = {
    #         "phone": "Введите номер в формате +71234567890",
    #     }


class UpdateEmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ["employment", "town_id", "address", "phone", "email", "website", "body", "location"]

        labels = {
            "employment": "Название организации",
            "town_id": "Расположение организации",
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
            "employment_id",
            "town_id",
            "skills_id",
            "body",
            "employer_id",
            "is_published",
        ]
        widgets = {
            # "skills_id": forms.CheckboxSelectMultiple(),
            "skills_id": forms.SelectMultiple(),
            # "employer_id": forms.HiddenInput(),
        }


class UpdateVacancyForm(forms.ModelForm):
    class Meta:
        model = VacancyHeader
        fields = [
            "job_title",
            "salary",
            "experience",
            "employment_id",
            "town_id",
            "skills_id",
            "body",
            "employer_id",
            "is_published",
        ]
        widgets = {
            # "skills_id": forms.CheckboxSelectMultiple(),
            "skills_id": forms.SelectMultiple(),
        }
