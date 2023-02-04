from django import forms
from employerapp.models import *


class AddEmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ["employment", "town_id", "address", "phone", "email", "website", "body", "location", "slug",
                  "user"]
        labels = {
            'employment': 'Название организации',
            'town_id': 'Расположение организации',
            'location': 'Место расположения организации на карте'
        }
        widgets = {
            'employment': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
            'address': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
        }

        help_texts = {'phone': 'Введите номер в формате +71234567890', }


class AddVacancyForm(forms.ModelForm):
    class Meta:
        model = VacancyHeader
        fields = ["job_title", "salary", "experience", "employment_id", "town_id", "skills_id",
                  "employer_id", "is_published"]


class UpdateEmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ["employment", "town_id", "address", "phone", "email", "website", "body", "location", "slug",
                  "user"]