from datetime import date

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.functional import cached_property

from outdoor_buddy.accounts.choices import (
    GenderChoices,
    SkillLevelChoices,
    FitnessLevelChoices,
)
from outdoor_buddy.events.models.activity import Activity
from outdoor_buddy.utils.validators import FileSizeValidator
from services.storage import DebuggableS3Storage

UserModel = get_user_model()


class Profile(models.Model):
    """
    Represents the user profile for the Outdoor Buddy application.
    Contains personal details, preferences, and additional information
    related to outdoor activities.
    """

    MAX_LENGTHS = {
        "name": 32,
    }
    MIN_LENGTH = {
        "name": 2,
    }

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ["user__email"]

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=MAX_LENGTHS["name"],
        null=True,
        blank=True,
        validators=[
            validators.MinLengthValidator(MIN_LENGTH["name"]),
            validators.RegexValidator(r"^[A-Za-z]*$", "Only letters are allowed."),
        ],
    )

    last_name = models.CharField(
        max_length=MAX_LENGTHS["name"],
        null=True,
        blank=True,
        validators=[
            validators.MinLengthValidator(MIN_LENGTH["name"]),
            validators.RegexValidator(r"^[A-Za-z]*$", "Only letters are allowed."),
        ],
    )

    gender = models.CharField(
        max_length=max(len(choice) for choice in GenderChoices.values),
        choices=GenderChoices.choices,
        default=GenderChoices.DO_NOT_SHOW,
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(null=True, blank=True)

    picture_upload = models.ImageField(
        upload_to="profile_pictures/",
        storage=DebuggableS3Storage(),
        validators=[
            FileSizeValidator(5),
        ],
        null=True,
        blank=True,
    )

    skill_level = models.CharField(
        max_length=max(len(choice) for choice in SkillLevelChoices.values),
        choices=SkillLevelChoices.choices,
        default=SkillLevelChoices.BEGINNER,
        null=True,
        blank=True,
    )

    fitness_level = models.CharField(
        max_length=max(len(choice) for choice in FitnessLevelChoices.values),
        choices=FitnessLevelChoices.choices,
        default=FitnessLevelChoices.MODERATE,
        null=True,
        blank=True,
    )

    preferred_activities = models.ManyToManyField(to=Activity, related_name="users")
    availability = models.TextField(null=True, blank=True)
    preferred_location = models.CharField(max_length=255, null=True, blank=True)
    languages = models.CharField(max_length=255, null=True, blank=True)
    outdoor_experience = models.TextField(null=True, blank=True)

    bio = models.TextField(null=True, blank=True)

    @cached_property
    def full_name(self):
        """
        Returns the user's full name by combining first and last names.
        If one is missing, returns the available name.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.first_name or self.last_name

    @property
    def age(self):
        """
        Calculates the user's age based on their date of birth.
        Returns an empty string if the date of birth is not provided.
        """
        if not self.date_of_birth:
            return ""
        today = date.today()
        age = (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
        return age

    def __str__(self):
        """
        Returns a string representation of the user's profile,
        displaying their full name and indicating if a name is not available.
        """
        return f"{self.full_name}'s Profile"
