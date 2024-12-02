from django.db import models


class StatusChoices(models.TextChoices):
    PENDING = "Pending", "Pending"
    ACCEPTED = "Accepted", "Accepted"
    DECLINED = "Declined", "Declined"

