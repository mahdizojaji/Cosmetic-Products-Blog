# Generated by Django 3.2.8 on 2021-11-17 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211116_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_img',
            field=models.ImageField(blank=True, null=True, upload_to='users/avatars/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cover_img',
            field=models.ImageField(blank=True, null=True, upload_to='users/covers/'),
        ),
    ]