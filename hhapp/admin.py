from django.contrib import admin
from hhapp.models import *

# Register your models here.

# admin.AdminSite.site_header = 'Административный раздел сайта GBdev2Python'

# Вакансия
@admin.register(VacancyHeader)
class VacancyHeaderAdmin(admin.ModelAdmin):
    list_display = ["job_title", "salary", "work_experience_id"]
    search_fields = ["job_title", "salary"]


# Работодатель
@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ["employment"]
    search_fields = ["employment"]
    prepopulated_fields = {"slug": ("employment", "town_id", )}


# 111111
@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    list_display = ["town"]
    search_fields = ["town"]


# Вид занятости
@admin.register(TypeEmployment)
class TypeEmploymentAdmin(admin.ModelAdmin):
    list_display = ["employment"]
    search_fields = ["employment"]


# График рабочего дня
@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ["working_day"]
    search_fields = ["working_day"]


# Опыт работы
@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ["work_experience"]
    search_fields = ["work_experience"]


# Перечисляемые разделы вакансии
@admin.register(VacancyBody)
class VacancyBodyAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]
