import django_filters
from employerapp.models import VacancyHeader


class VacancyFilter(django_filters.FilterSet):
    salary = django_filters.RangeFilter()

    class Meta:
        model = VacancyHeader
        fields = ('salary', 'experience', 'employment_id', 'town_id', 'skills_id', 'employer_id')
