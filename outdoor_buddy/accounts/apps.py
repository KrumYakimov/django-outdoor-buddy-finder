from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "outdoor_buddy.accounts"

    def ready(self):
        import outdoor_buddy.accounts.signals

