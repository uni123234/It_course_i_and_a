# Generated by Django 5.0.6 on 2024-06-30 16:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("course", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="HelpRequest",
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
                ("request", models.TextField()),
                ("status", models.CharField(default="pending", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.course"
                    ),
                ),
            ],
        ),
    ]
