from django.db import models


class SkillLevelChoices(models.TextChoices):
    BEGINNER = "Beginner", "Beginner"
    INTERMEDIATE = "Intermediate", "Intermediate"
    ADVANCED = "Advanced", "Advanced"
    EXPERT = "Expert", "Expert"


class FitnessLevelChoices(models.TextChoices):
    LOW = "Low", "Low"
    MODERATE = "Moderate", "Moderate"
    HIGH = "High", "High"
    ATHLETE = "Athlete", "Athlete"

