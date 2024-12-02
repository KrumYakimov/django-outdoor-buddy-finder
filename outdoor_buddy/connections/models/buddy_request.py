from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

from outdoor_buddy.connections.choices import StatusChoices


UserModel = get_user_model()


class BuddyRequest(models.Model):
    """
    This model tracks connection requests between two users. It includes information about:

        - Who sent the request (from_user).
        - Who received the request (to_user).
        - The status of the request (e.g., pending, accepted, declined).

    """

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_requests"
    )
    to_user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="received_requests"
    )
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
