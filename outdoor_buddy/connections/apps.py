from django.apps import AppConfig


class ConnectionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "outdoor_buddy.connections"

    def ready(self):
        import outdoor_buddy.connections.signals
