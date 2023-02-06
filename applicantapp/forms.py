from django import forms
from django.forms import ModelForm

from .models import Resumes


class ResumeForm(ModelForm):
    class Meta:
        model = Resumes
        fields = ["applicants", "required_job", "image", "skills", "salary", "last_job", "education", "is_published"]
        widgets = {
            "skills": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
