# Generated by Django 5.0.6 on 2024-07-01 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edit_password", "0002_passwordchangerequest_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="passwordchangerequest",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]