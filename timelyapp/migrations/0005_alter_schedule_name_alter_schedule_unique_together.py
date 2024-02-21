# Generated by Django 5.0.1 on 2024-02-21 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("timelyapp", "0004_rename_user_id_schedule_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="schedule",
            name="name",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name="schedule",
            unique_together={("user", "name")},
        ),
    ]
