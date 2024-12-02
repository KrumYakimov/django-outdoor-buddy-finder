from django.contrib.auth import get_user_model
from django.db import models

from outdoor_buddy.events.models import Event

UserModel = get_user_model()


class EventParticipant(models.Model):
    event = models.ForeignKey(
        to=Event, on_delete=models.CASCADE, related_name="participants"
    )
    user = models.ForeignKey(
        to=UserModel, on_delete=models.CASCADE, related_name="participated_events"
    )
    joined_at = models.DateTimeField(auto_now_add=True)
