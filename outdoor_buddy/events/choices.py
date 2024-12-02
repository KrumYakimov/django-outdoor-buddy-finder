from django.db import models


class RegistrationSatusChoices(models.TextChoices):
    OPEN = "Open", "Open"
    CLOSED = "Closed", "Closed"
