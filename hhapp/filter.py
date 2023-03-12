import django_filters
from employerapp.models import VacancyHeader, TypeEmployment
from applicantapp.models import Resumes, Skill
from django import forms


class VacancyFilter(django_filters.FilterSet):
    salary__gt = django_filters.NumberFilter(field_name='salary', lookup_expr='gt', label='Заработная плата от')
    salary__lt = django_filters.NumberFilter(field_name='salary', lookup_expr='lt', label='до')
    employment = django_filters.ModelMultipleChoiceFilter(queryset=TypeEmployment.objects.all(), widget=forms.CheckboxSelectMultiple)
    skills = django_filters.ModelMultipleChoiceFilter(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple)
    employer_id = django_filters.CharFilter(field_name='employer_id__employment', lookup_expr='icontains', label='Работодатель')
    class Meta:
        model = VacancyHeader
        fields = ('salary__gt', 'salary__lt', 'experience', 'employment', 'town', 'skills', 'employer_id')

class ResumeFilter(django_filters.FilterSet):
    salary__gt = django_filters.NumberFilter(field_name='salary', lookup_expr='gt', label='Заработная плата от')
    salary__lt = django_filters.NumberFilter(field_name='salary', lookup_expr='lt', label='до')
    skills = django_filters.ModelMultipleChoiceFilter(queryset=Skill.objects.all(),
                                                         widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Resumes
        fields = ('salary__gt', 'salary__lt', 'skills', 'town_job')
