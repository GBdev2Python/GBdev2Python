from django import forms
from django.forms import ModelForm

from .models import Resumes, Applicants


class ResumeForm(ModelForm):
    class Meta:
        model = Resumes
        fields = ["required_job", "image", "skills", "salary", "last_job", "education", "is_published"]

        widgets = {
            "skills": forms.CheckboxSelectMultiple(),
            # 'image': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class AddApplicateForm(forms.ModelForm):

    class Meta:
        model = Applicants
        fields = ["first_name", "last_name", "birthday", "town", "phone", "user"]

        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "birthday": "Дата рождения",
            "town": "Город (населенный пункт)",
        }

