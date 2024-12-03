from django.db import models

from outdoor_buddy.utils.choices import SkillLevelChoices, FitnessLevelChoices
from outdoor_buddy.utils.validators import FileSizeValidator
from services.storage import S3Storage


class TimestampedModelMixin(models.Model):
    """
    Abstract mixin that adds `created_at` and `updated_at` timestamp fields
    to any model that inherits from it.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImageUploadMixin(models.Model):
    picture_upload = models.ImageField(
        upload_to="profile_pictures/",
        storage=S3Storage(),
        validators=[
            FileSizeValidator(5),
        ],
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class CapabilityLevelMixinMixin(models.Model):

    skill_level = models.CharField(
        max_length=max(len(choice) for choice in SkillLevelChoices.values),
        choices=SkillLevelChoices.choices,
        null=True,
        blank=True,
    )

    fitness_level = models.CharField(
        max_length=max(len(choice) for choice in FitnessLevelChoices.values),
        choices=FitnessLevelChoices.choices,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

