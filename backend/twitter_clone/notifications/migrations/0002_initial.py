# Generated by Django 4.2.3 on 2023-10-07 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("notifications", "0001_initial"),
        ("tweets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="comment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="tweets.comment",
            ),
        ),
    ]
