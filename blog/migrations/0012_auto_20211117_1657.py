# Generated by Django 3.2.8 on 2021-11-17 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20211117_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='rate',
        ),
        migrations.RemoveField(
            model_name='course',
            name='rate_counts',
        ),
        migrations.RemoveField(
            model_name='course',
            name='rate_points',
        ),
    ]
