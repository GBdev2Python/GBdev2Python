from django.contrib import admin

from serviceapp import models

# Register your models here.


@admin.register(models.Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ["id", "cover_letter", "resume", "vacancyheader", "status", "created_at", "updated_at"]
    ordering = ["-updated_at"]
