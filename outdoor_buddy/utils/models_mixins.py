from django.db import models


class TimestampedModelMixin(models.Model):
    """
    Abstract mixin that adds `created_at` and `updated_at` timestamp fields
    to any model that inherits from it.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
