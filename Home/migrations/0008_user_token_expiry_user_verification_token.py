# Generated by Django 4.1.13 on 2025-05-18 16:56

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0007_user_created_at_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token_expiry',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='user',
            name='verification_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
