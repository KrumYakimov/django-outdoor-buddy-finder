from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from outdoor_buddy.events.choices import RegistrationSatusChoices
from outdoor_buddy.events.models import Activity
from outdoor_buddy.utils.models_mixins import ImageUploadMixin, CapabilityLevelMixinMixin


UserModel = get_user_model()


class Event(ImageUploadMixin, CapabilityLevelMixinMixin):
    """
    This model represents an event where users can participate.
    It includes essential details about the event, such as timing, location, and activity type,
    as well as participation-related information like capacity, spots remaining, and registration status.
    """

    # Essential Event Details
    name = models.CharField(max_length=50, unique=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=255)
    embedded_map = models.URLField(blank=True, null=True)  # Optional
    description = models.TextField()
    activity_type = models.ForeignKey(
        to=Activity, on_delete=models.CASCADE, related_name="events"
    )
    capacity = models.PositiveIntegerField()
    spots_remaining = models.PositiveIntegerField(
        blank=True, null=True
    )  # Calculated dynamically if needed

    # Organizer Details
    creator = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="created_events",
    )
    registration_deadline = models.DateTimeField(blank=True, null=True)
    registration_status = models.CharField(
        max_length=max(len(choice) for choice in RegistrationSatusChoices.values),
        choices=RegistrationSatusChoices.choices,
        default=RegistrationSatusChoices.OPEN,
    )

    def __str__(self):
        return f"{self.activity_type.name} - {self.description[:30]}"

    def save(self, *args, **kwargs):
        """
        Initializes the `spots_remaining` field to the value of `capacity`
        if not explicitly set, ensuring available spots start with the event's capacity.
        """
        if self.spots_remaining is None:  # Initialize spots_remaining to capacity
            self.spots_remaining = self.capacity
        super().save(*args, **kwargs)
