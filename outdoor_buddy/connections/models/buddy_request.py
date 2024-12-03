from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

from outdoor_buddy.connections.choices import StatusChoices
from outdoor_buddy.utils.models_mixins import TimestampedModelMixin

UserModel = get_user_model()


class BuddyRequest(TimestampedModelMixin):
    """
    This model tracks connection requests between two users. It includes information about:

        - Who sent the request (from_user).
        - Who received the request (to_user).
        - The status of the request (e.g., pending, accepted, declined).

    """

    from_user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="sent_requests"
    )
    to_user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="received_requests"
    )
    status = models.CharField(
        max_length=max(len(choice) for choice in StatusChoices.values),
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    class Meta:
        unique_together = ("from_user", "to_user")  # Prevent duplicate requests
        verbose_name = "Buddy Request"
        verbose_name_plural = "Buddy Requests"
        # Ensure a user cannot send a request to themselves
        constraints = [
            models.CheckConstraint(
                check=~models.Q(from_user=models.F("to_user")),
                name="prevent_self_request",
            )
        ]

    def __str__(self):
        """
        Returns a string representation of the buddy request
        """
        return f"{self.from_user} -> {self.to_user} ({self.status})"
