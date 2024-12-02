from django.contrib.auth import get_user_model
from django.db import models


UserModel = get_user_model()


class Connection(models.Model):
    """
    Tracks approved buddy connections between two users.
    Each connection is mutual, meaning user1 is connected to user2 and vice versa.
    """
    user1 = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="connections_as_user1"
    )
    user2 = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="connections_as_user2"
    )
    connected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")  # Prevent duplicate connections
        verbose_name = "Connection"
        verbose_name_plural = "Connections"
        # Ensure a user cannot connect to themselves
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user1=models.F("user2")),
                name="prevent_self_connection"
            )
        ]
        # An index for better query performance
        indexes = [
            models.Index(fields=["user1", "user2"], name="connection_index")
        ]

    def __str__(self):
        """
        Returns a string representation of the connection.
        """
        return f"{self.user1} <-> {self.user2}"

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure connections are always stored with user1's ID less than user2's ID.
        This enforces consistency and avoids duplicate pairs in reverse order (e.g., A->B and B->A).
        """
        if self.user1 and self.user2 and self.user1.pk > self.user2.pk:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

