from django.db import models


class GenderChoices(models.TextChoices):
    MALE = "Male", "Male"
    FEMALE = "Female", "Female"
    DO_NOT_SHOW = "Do not show", "Do not show"

