from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "outdoor_buddy.events"

    def ready(self):
        import outdoor_buddy.events.signals


