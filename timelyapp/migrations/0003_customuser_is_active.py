# Generated by Django 5.0.1 on 2024-02-03 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("timelyapp", "0002_customuser_is_staff_customuser_is_superuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
