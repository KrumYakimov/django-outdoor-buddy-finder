# Generated by Django 5.1.3 on 2024-11-29 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_profile_fitness_level_alter_profile_gender_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="nationality",
        ),
    ]
