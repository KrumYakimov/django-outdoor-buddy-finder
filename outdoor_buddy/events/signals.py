from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from outdoor_buddy.events.models.event_participant import EventParticipant


@receiver(post_save, sender=EventParticipant)
@receiver(post_delete, sender=EventParticipant)
def update_spots_remaining(sender, instance, **kwargs):
    event = instance.event
    event.spots_remaining = event.capacity - event.participants.count()
    event.save()
