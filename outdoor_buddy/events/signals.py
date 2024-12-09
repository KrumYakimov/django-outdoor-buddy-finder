import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from outdoor_buddy.events.models.event_participant import EventParticipant


logger = logging.getLogger(__name__)


@receiver(post_save, sender=EventParticipant)
@receiver(post_delete, sender=EventParticipant)
def update_spots_remaining(sender, instance, **kwargs):
    """
    Updates the `spots_remaining` field of an Event after a participant
    is added or removed by recalculating based on the event's capacity.
    """
    logger.info(f"Signal triggered for event: {instance.event}")
    event = instance.event
    event.spots_remaining = event.capacity - event.participants.count()
    event.save()
    logger.info(f"Updated spots_remaining for event {event.id}: {event.spots_remaining}")


