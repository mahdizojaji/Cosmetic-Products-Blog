# Generated by Django 3.2.8 on 2021-11-30 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_alter_course_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='edited_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='edited_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]