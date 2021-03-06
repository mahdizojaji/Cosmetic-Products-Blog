# Generated by Django 3.2.8 on 2021-11-15 13:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211112_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID'),
        ),
    ]
