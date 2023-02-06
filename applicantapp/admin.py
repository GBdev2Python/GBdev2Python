from django.contrib import admin

from applicantapp.models import Applicants, Resumes, Skill, Towns

# Register your models here.


admin.site.register(Resumes)
admin.site.register(Skill)
admin.site.register(Towns)
admin.site.register(Applicants)
