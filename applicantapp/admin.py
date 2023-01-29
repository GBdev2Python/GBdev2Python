from django.contrib import admin
from applicantapp.models import Skill,Towns, Applicants, Resumes
# Register your models here.


admin.site.register(Resumes)
admin.site.register(Skill)
admin.site.register(Towns)
admin.site.register(Applicants)
