# Generated by Django 5.0.7 on 2024-11-02 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_homework_lesson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='course',
        ),
        migrations.AddField(
            model_name='course',
            name='groups',
            field=models.ManyToManyField(related_name='courses', to='api.group'),
        ),
    ]
