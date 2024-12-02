from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Review


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("reviewer", "event", "user", "rating", "created_at")
    list_filter = ("rating", "created_at", "updated_at")
    search_fields = ("reviewer__username", "event__name", "user__username", "comment")
    ordering = ("-created_at",)
    layout = (
        ("Review Details", {
            "fields": ("reviewer", "event", "user", "rating", "comment"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )
