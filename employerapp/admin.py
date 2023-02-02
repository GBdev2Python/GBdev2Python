
from django.contrib import admin
from employerapp.models import *


# Register your models here.

admin.AdminSite.site_header = 'Административный раздел сайта'

# Вакансия
@admin.register(VacancyHeader)
class VacancyHeaderAdmin(admin.ModelAdmin):
    list_display = ["job_title", "employer_id", "created", "is_published", "experience"]

    # list_display_links = ("job_title", "employer_id",)
    list_editable = ["is_published", "experience"]
    search_fields = ("job_title", "salary",)
    list_filter = ('employer_id',)
    filter_horizontal = ["employment_id"]


# Работодатель
@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ["employment"]
    search_fields = ["employment"]
    prepopulated_fields = {"slug": ("employment", "user",)}


# Вид занятости
@admin.register(TypeEmployment)
class TypeEmploymentAdmin(admin.ModelAdmin):
    list_display = ["employment"]
    search_fields = ["employment"]


# # График рабочего дня
# @admin.register(WorkingDay)
# class WorkingDayAdmin(admin.ModelAdmin):
#     list_display = ["working_day"]
#     search_fields = ["working_day"]


# # Опыт работы
# @admin.register(WorkExperience)
# class WorkExperienceAdmin(admin.ModelAdmin):
#     list_display = ["work_experience"]
#     search_fields = ["work_experience"]


# Перечисляемые разделы вакансии
@admin.register(VacancyBody)
class VacancyBodyAdmin(admin.ModelAdmin):
    list_display = ["vacancy_header_id", "title", "ranking"]
    list_display_links = ('vacancy_header_id', "title",)
    search_fields = ["title"]
    list_editable = ["ranking"]
    list_filter = ('vacancy_header_id',)
