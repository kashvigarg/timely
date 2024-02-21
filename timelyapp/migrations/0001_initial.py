# Generated by Django 5.0.1 on 2024-02-21 14:09

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("username", models.CharField(max_length=30, unique=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Schedule",
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
                ("name", models.CharField(default="", max_length=255, unique=True)),
                ("duration", models.IntegerField(default=0)),
                ("starts_on", models.DateTimeField(default=django.utils.timezone.now)),
                ("no_of_tasks", models.IntegerField(default=0)),
                (
                    "longest_sitting_time",
                    models.DurationField(default=datetime.timedelta(seconds=7200)),
                ),
                (
                    "behaviour",
                    models.IntegerField(
                        choices=[
                            (1, "LAZY"),
                            (2, "MODERATELY_LAZY"),
                            (3, "MODERATELY_HARDWORKING"),
                            (4, "HARDWORKING"),
                        ],
                        default=3,
                    ),
                ),
                ("has_timetable", models.BooleanField(default=False)),
                ("schedule_color", models.CharField(default="#9292F0", max_length=255)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
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
                ("name", models.CharField(default="", max_length=255)),
                (
                    "difficulty",
                    models.IntegerField(
                        choices=[(1, "HARD"), (2, "MEDIUM"), (3, "EASY")], default=3
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        choices=[(1, "HIGH"), (2, "MEDIUM"), (3, "LOW")], default=2
                    ),
                ),
                ("no_of_revisions", models.IntegerField(default=0)),
                ("estimated_length", models.DurationField(default=datetime.timedelta)),
                (
                    "schedule_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="timelyapp.schedule",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TimeTable",
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
                (
                    "timetable_color",
                    models.CharField(default="#9292F0", max_length=255),
                ),
                (
                    "schedule_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="timelyapp.schedule",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TimeSlab",
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
                ("start_time", models.TimeField(default=django.utils.timezone.now)),
                ("end_time", models.TimeField(default=django.utils.timezone.now)),
                ("timeslab_color", models.CharField(default="#9292F0", max_length=255)),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("day", models.CharField(default="", max_length=255)),
                (
                    "task_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="timelyapp.task"
                    ),
                ),
                (
                    "timetable_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="timelyapp.timetable",
                    ),
                ),
            ],
        ),
    ]
