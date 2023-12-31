# Generated by Django 4.2.3 on 2023-10-07 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("chat", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="privatechat",
            name="connected_users",
            field=models.ManyToManyField(
                blank=True, related_name="connected_users", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="privatechat",
            name="user1",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user1",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="privatechat",
            name="user2",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user2",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="chat.privatechat"
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
