# Generated by Django 3.2.8 on 2021-11-29 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_article_premium'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Published')], default=1),
        ),
    ]