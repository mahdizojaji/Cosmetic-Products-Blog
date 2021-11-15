# Generated by Django 3.2.8 on 2021-11-15 13:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20211109_2323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='slug_title',
            new_name='slug',
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='article',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID'),
        ),
    ]
