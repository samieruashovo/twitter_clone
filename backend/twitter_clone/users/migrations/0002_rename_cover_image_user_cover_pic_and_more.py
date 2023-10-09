# Generated by Django 4.2.3 on 2023-10-07 12:01

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="cover_image",
            new_name="cover_pic",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="nickname",
            new_name="gender",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="avatar",
            new_name="profile_pic",
        ),
        migrations.AddField(
            model_name="user",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="user",
            name="followers",
            field=models.ManyToManyField(
                blank=True, related_name="followedme", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]