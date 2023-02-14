from django.contrib import admin

from employerapp.models import *

# Register your models here.

admin.AdminSite.site_header = "Административный раздел сайта"

# Вакансия
@admin.register(VacancyHeader)
class VacancyHeaderAdmin(admin.ModelAdmin):
    list_display = ["job_title", "employer_id", "experience", "salary", "created", "is_published"]
    list_editable = ["experience", "salary", "is_published"]
    search_fields = (
        "job_title",
        "salary",
    )
    list_filter = ("employer_id",)
    filter_horizontal = ["employment_id", "skills_id"]


# Работодатель
@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ["employment"]
    search_fields = ["employment"]
    # prepopulated_fields = {
    #     "slug": (
    #         "employment",
    #         "user",
    #     )
    # }


# Вид занятости
@admin.register(TypeEmployment)
class TypeEmploymentAdmin(admin.ModelAdmin):
    list_display = ["employment"]
    search_fields = ["employment"]
