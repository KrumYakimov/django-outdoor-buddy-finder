from django.contrib import admin
from unfold.admin import ModelAdmin

from outdoor_buddy.events.models import Activity, Event, EventParticipant


@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = (
        "activity_type",
        "start_datetime",
        "end_datetime",
        "location",
        "capacity",
        "spots_remaining",
        "creator",
        "registration_status",
    )
    list_filter = ("activity_type", "skill_level", "fitness_level", "registration_status")
    search_fields = (
        "activity_type__name",
        "description",
        "location",
        "creator__username",
    )
    ordering = ("start_datetime",)
    layout = (
        (
            "Event Details",
            {
                "fields": (
                    "activity_type",
                    "start_datetime",
                    "end_datetime",
                    "location",
                    "embedded_map",
                    "description",
                ),
            },
        ),
        (
            "Capacity and Registration",
            {
                "fields": (
                    "capacity",
                    "spots_remaining",
                    "registration_status",
                    "registration_deadline",
                ),
            },
        ),
        (
            "Organizer",
            {
                "fields": ("creator",),
            },
        ),
    )


@admin.register(EventParticipant)
class EventParticipantAdmin(ModelAdmin):
    list_display = ("event", "user", "joined_at")
    list_filter = ("event",)
    search_fields = ("event__description", "user__username")
    layout = (
        (
            "Participant Details",
            {
                "fields": ("event", "user"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("joined_at",),
            },
        ),
    )
