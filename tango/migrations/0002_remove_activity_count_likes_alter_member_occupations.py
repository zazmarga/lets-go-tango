# Generated by Django 5.1.3 on 2024-11-14 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tango", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="activity",
            name="count_likes",
        ),
        migrations.AlterField(
            model_name="member",
            name="occupations",
            field=models.ManyToManyField(related_name="members", to="tango.occupation"),
        ),
    ]
