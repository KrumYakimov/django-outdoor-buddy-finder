# Generated by Django 5.1.3 on 2024-12-02 15:18

import django.db.models.deletion
import outdoor_buddy.utils.validators
import services.storage
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Activity",
                "verbose_name_plural": "Activities",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "picture_upload",
                    models.ImageField(
                        blank=True,
                        null=True,
                        storage=services.storage.S3Storage(),
                        upload_to="profile_pictures/",
                        validators=[
                            outdoor_buddy.utils.validators.FileSizeValidator(5)
                        ],
                    ),
                ),
                (
                    "skill_level",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Beginner", "Beginner"),
                            ("Intermediate", "Intermediate"),
                            ("Advanced", "Advanced"),
                            ("Expert", "Expert"),
                        ],
                        max_length=12,
                        null=True,
                    ),
                ),
                (
                    "fitness_level",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Low", "Low"),
                            ("Moderate", "Moderate"),
                            ("High", "High"),
                            ("Athlete", "Athlete"),
                        ],
                        max_length=8,
                        null=True,
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("start_datetime", models.DateTimeField()),
                ("end_datetime", models.DateTimeField()),
                ("location", models.CharField(max_length=255)),
                ("embedded_map", models.URLField(blank=True, null=True)),
                ("description", models.TextField()),
                ("capacity", models.PositiveIntegerField()),
                ("spots_remaining", models.PositiveIntegerField(blank=True, null=True)),
                ("registration_deadline", models.DateTimeField(blank=True, null=True)),
                (
                    "registration_status",
                    models.CharField(
                        choices=[("Open", "Open"), ("Closed", "Closed")],
                        default="Open",
                        max_length=6,
                    ),
                ),
                (
                    "activity_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="events.activity",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EventParticipant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participants",
                        to="events.event",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participated_events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
