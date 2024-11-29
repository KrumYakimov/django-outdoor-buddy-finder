from django.contrib import admin
from unfold.admin import ModelAdmin

from outdoor_buddy.events.models import Activity


@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)

