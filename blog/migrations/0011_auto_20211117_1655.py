# Generated by Django 3.2.8 on 2021-11-17 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20211117_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='image',
        ),
        migrations.RemoveField(
            model_name='article',
            name='slug_title',
        ),
        migrations.AddField(
            model_name='course',
            name='rate',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
        migrations.AddField(
            model_name='course',
            name='rate_counts',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='rate_points',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
