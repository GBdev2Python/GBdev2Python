from django import forms
from django.forms import ModelForm

from .models import Resumes, Applicants, ResumeInvitation, Experience


class ResumeForm(ModelForm):
    class Meta:
        model = Resumes
        fields = ["required_job", "image", "skills", "salary", "town_job", "education", "is_published"]
        widgets = {
            'skills': forms.CheckboxSelectMultiple(),
            'image': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class EditApplicantForm(ModelForm):
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


class InvitationCreationForm(ModelForm):

    class Meta:
        model = ResumeInvitation
        fields = ['resume', 'vacancy', 'cover_letter']
        widgets = {
            'resume': forms.HiddenInput,
        }


class ExperienceForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'formCompanyFields'

    class Meta:
        model = Experience
        fields = ['company', 'description']
        widgets = {
            'description': forms.Textarea(attrs={"rows": 5}),
        }


class ExperienceEditForm(ModelForm):

    field_order = ['company', 'description']

    class Meta:
        model = Experience
        fields = ['company', 'description']
        widgets = {
            'company': forms.TextInput(),
            'description': forms.Textarea(attrs={"rows": 5})
        }


ExperienceFormSet = forms.formset_factory(ExperienceForm)
ExperienceEditFormset = forms.modelformset_factory(Experience, form=ExperienceForm)
