from django.contrib import admin

from applicantapp.models import Applicants, Resumes, Skill, Towns


# Register your models here.
class ApplicantsAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_display_links = ("id",)


admin.site.register(Resumes)
admin.site.register(Skill)
admin.site.register(Towns)
admin.site.register(Applicants, ApplicantsAdmin)
