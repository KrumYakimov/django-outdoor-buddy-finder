# Generated by Django 5.1.3 on 2024-12-02 10:02

import outdoor_buddy.utils.validators
import services.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_event_eventparticipant"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="picture_upload",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=services.storage.DebuggableS3Storage(),
                upload_to="profile_pictures/",
                validators=[outdoor_buddy.utils.validators.FileSizeValidator(5)],
            ),
        ),
    ]
