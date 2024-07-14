from django.db import migrations, models
import datetime


def get_default_created_at():
    return datetime.datetime.now().isoformat()


class Migration(migrations.Migration):

    dependencies = [
        ("edit_email", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="emailchangerequest",
            name="created_at",
            field=models.DateTimeField(default=get_default_created_at),
            preserve_default=False,
        ),
    ]