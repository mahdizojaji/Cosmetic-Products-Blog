# Generated by Django 3.2.8 on 2021-11-22 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='comment_qty',
            field=models.BigIntegerField(blank=True, default=0),
        ),
    ]