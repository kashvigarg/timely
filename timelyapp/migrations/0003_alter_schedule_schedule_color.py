# Generated by Django 5.0.1 on 2024-02-12 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("timelyapp", "0002_schedule_has_timetable_schedule_schedule_color_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="schedule",
            name="schedule_color",
            field=models.CharField(default="#9292F0FE", max_length=255),
        ),
    ]
