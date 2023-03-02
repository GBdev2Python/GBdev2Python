from django import forms
from django.forms import ModelForm

from .models import Resumes, Applicants


class ResumeForm(ModelForm):
    class Meta:
        model = Resumes
        fields = ["required_job", "image", "skills", "salary", "town_job", "last_job", "education", "is_published"]

        widgets = {
            'skills': forms.CheckboxSelectMultiple(),
            'image': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class EditApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicants
        fields = ["image", "first_name", "last_name", "birthday", "town", "phone"]
        labels = {
            "image": "Аватар",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "birthday": "Дата рождения",
            "town": "Город (населенный пункт)",
        }
