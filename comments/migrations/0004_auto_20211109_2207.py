# Generated by Django 3.2.8 on 2021-11-09 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('comments', '0003_alter_comment_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rate',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ['article']}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
    ]
