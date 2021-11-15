# Generated by Django 3.2.8 on 2021-11-15 13:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_alter_article_bookmarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='article_bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]
