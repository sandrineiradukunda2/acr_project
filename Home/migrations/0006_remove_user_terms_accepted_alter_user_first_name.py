# Generated by Django 5.2 on 2025-05-10 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_alter_user_first_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='terms_accepted',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
    ]
