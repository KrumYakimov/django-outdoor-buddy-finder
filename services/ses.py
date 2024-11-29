import logging
import boto3
from botocore.exceptions import ClientError
from django.core.exceptions import ValidationError
from django.conf import settings

logger = logging.getLogger('outdoor_buddy')


class SESService:
    def __init__(self):
        self.ses_client = boto3.client(
            "ses",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET,
            region_name=settings.AWS_REGION,
        )

    def send_email(self, recipient, subject, plain_text=None, html_content=None):
        """
        Sends an email via AWS SES with optional plain-text and HTML content.
        """
        sender = settings.EMAIL_SENDER

        # Build the email body
        body = {}
        if plain_text:
            body["Text"] = {"Data": plain_text, "Charset": "UTF-8"}
        if html_content:
            body["Html"] = {"Data": html_content, "Charset": "UTF-8"}

        try:
            self.ses_client.send_email(
                Source=sender,
                Destination={"ToAddresses": [recipient]},
                Message={
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": body,
                },
            )
            logger.info(f"Email sent successfully to {recipient}")
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            logger.error(f"Failed to send email to {recipient}: {error_message}")
            raise ValidationError(f"Failed to send email: {error_message}")


def send_email_to_user(user, subject, plain_text=None, html_content=None):
    """
    General-purpose function to send an email to a user via SES.
    """
    ses_service = SESService()

    ses_service.send_email(
        recipient=user.email,
        subject=subject,
        plain_text=plain_text,
        html_content=html_content,
    )


