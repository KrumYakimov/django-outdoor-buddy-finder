import logging

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from outdoor_buddy.accounts.models import Profile, Contact
from outdoor_buddy.utils.email_templates import EmailTemplates
from services.ses import send_email_to_user

logger = logging.getLogger('outdoor_buddy')

UserModel = get_user_model()


def send_welcome_email_to_user(user):
    subject = EmailTemplates.SUBJECT_WELCOME_EMAIL
    plain_text = EmailTemplates.PLAIN_TEXT_CONTENT_WELCOME.format(email=user.email)
    html_content = EmailTemplates.HTML_TEXT_CONTENT_WELCOME.format(email=user.email)
    send_email_to_user(user, subject, plain_text=plain_text, html_content=html_content)


@receiver(post_save, sender=UserModel)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        try:
            if not hasattr(instance, "profile"):
                Profile.objects.create(user=instance)
        except IntegrityError as e:
            logger.warning(f"Could not create profile for {instance.email}: {e}")

        try:
            if not hasattr(instance, "contact"):
                Contact.objects.create(user=instance)
        except IntegrityError as e:
            logger.warning(f"Could not create contact for {instance.email}: {e}")

        if not instance.is_staff:
            logger.info(
                f"Sending welcome email to {instance.email} (ID: {instance.id})"
            )
            try:
                send_welcome_email_to_user(instance)
            except Exception as e:
                logger.error(f"Failed to send welcome email to {instance.email}: {e}")
