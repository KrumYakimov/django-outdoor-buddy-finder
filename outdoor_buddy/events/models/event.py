from django.conf import settings
from django.db import models

from . import Activity
from ..choices import RegistrationSatusChoices


class Event(models.Model):
    # Essential Event Details
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=255)
    embedded_map = models.URLField(blank=True, null=True)  # Optional
    description = models.TextField()
    activity_type = models.ForeignKey(
        to=Activity, on_delete=models.CASCADE, related_name="events"
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("expert", "Expert"),
        ],
    )
    capacity = models.PositiveIntegerField()
    spots_remaining = models.PositiveIntegerField(
        blank=True, null=True
    )  # Calculated dynamically if needed

    # Organizer and Participation Details
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_events",
    )
    registration_deadline = models.DateTimeField(blank=True, null=True)
    registration_status = models.CharField(
        max_length=10,
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
