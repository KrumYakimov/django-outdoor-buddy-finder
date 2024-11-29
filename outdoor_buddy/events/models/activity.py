from django.db import models


class Activity(models.Model):

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ["name"]

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
