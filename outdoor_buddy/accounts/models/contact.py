from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

UserModel = get_user_model()


class Contact(models.Model):
    MAX_LENGTH = {"city": 32, "address": 64, "phone": 15}

    MIN_LENGTH = {"city": 2, "address": 4, "phone": 10}

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ["user__email"]

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    city = models.CharField(
        max_length=MAX_LENGTH["city"],
        validators=[
            validators.MinLengthValidator(MIN_LENGTH["city"]),
        ],
        null=True,
        blank=True,
    )

    address = models.CharField(
        max_length=MAX_LENGTH["address"],
        validators=[
            validators.MinLengthValidator(MIN_LENGTH["address"]),
        ],
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=MAX_LENGTH["phone"],
        null=True,
        blank=True,
        validators=[
            validators.MinLengthValidator(MIN_LENGTH["phone"]),
            validators.RegexValidator(
                regex=r"^0\d{9,14}$",
                message="Phone number must start with 0 and contain exactly 10 to 15 digits.",
            ),
        ],
    )

    @property
    def is_completed(self):
        return all([self.city, self.address, self.phone_number])

    def __str__(self):
        full_name = (
            self.user.profile.full_name
            if hasattr(self.user, "profile") and self.user.profile.full_name
            else "No name specified"
        )
        return f"{full_name} ({self.user}): Contact id: {self.pk}"
