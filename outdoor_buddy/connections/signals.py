import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from outdoor_buddy.connections.choices import StatusChoices
from outdoor_buddy.connections.models.buddy_request import BuddyRequest
from outdoor_buddy.connections.models.connection import Connection

logger = logging.getLogger(__name__)

UserModel = get_user_model()


@receiver(post_save, sender=BuddyRequest)
def create_connection_on_accept(sender, instance, **kwargs):
    """
    Automatically creates a Connection when a BuddyRequest is accepted.
    Ensures no duplicate connections are created.
    """
    if instance.status == StatusChoices.ACCEPTED:
        connection, created = Connection.objects.get_or_create(
            user1=min([instance.from_user, instance.to_user], key=lambda user: user.pk),
            user2=max([instance.from_user, instance.to_user], key=lambda user: user.pk),
        )
        if created:
            logger.info(
                f"Connection created between {connection.user1} and {connection.user2}."
            )
