from django.db import models


class Activity(models.Model):
    """
    This model represents different types of activities that events can be associated with.
    It includes a unique name for each activity and an optional description.
    """
    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ["name"]

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
