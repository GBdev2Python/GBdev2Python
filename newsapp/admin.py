from django.contrib import admin

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "url", "deleted")
    list_display_links = ("id",)
    list_filter = ("source",)

    search_fields = ("title", "content", "description", "source")
