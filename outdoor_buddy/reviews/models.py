from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from outdoor_buddy.events.models import Event
from outdoor_buddy.utils.models_mixins import TimestampedModelMixin

UserModel = get_user_model()


class Review(TimestampedModelMixin):
    """
    Represents a review left by a user for an event or another user.
    Includes rating, comments, and timestamps.
    """

    reviewer = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="given_reviews"
    )
    # A review can be for an event or a user
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="received_reviews",
        null=True,
        blank=True
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating must be between 1 (lowest) and 5 (highest)."
    )
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(event__isnull=False, user__isnull=True) |
                    models.Q(event__isnull=True, user__isnull=False)
                ),
                name="review_target_exclusivity"
            )
        ]

    def __str__(self):
        """
        Returns a string representation of the review, indicating the reviewer,
        the target (event or user), and the rating.
        """
        target = self.event if self.event else self.user
        return f"Review by {self.reviewer} for {target} - {self.rating}/5"
