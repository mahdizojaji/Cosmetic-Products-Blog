# Generated by Django 3.2.8 on 2021-11-02 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_org_article_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='parent',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.article'),
        ),
    ]
