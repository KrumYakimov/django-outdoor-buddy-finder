from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import BuddyRequest, Connection


@admin.register(BuddyRequest)
class BuddyRequestAdmin(ModelAdmin):
    list_display = ("from_user", "to_user", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("from_user__username", "to_user__username")
    layout = (
        (
            "Request Details",
            {
                "fields": ("from_user", "to_user", "status"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )


@admin.register(Connection)
class ConnectionAdmin(ModelAdmin):
    list_display = ("user1", "user2", "connected_at")
    list_filter = ("connected_at",)
    search_fields = ("user1__username", "user2__username")
    layout = (
        (
            "Connection Details",
            {
                "fields": ("user1", "user2"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("connected_at",),
            },
        ),
    )
