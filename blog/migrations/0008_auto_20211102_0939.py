# Generated by Django 3.2.8 on 2021-11-02 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_article_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='parent',
        ),
        migrations.AddField(
            model_name='article',
            name='original',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='clone', to='blog.article'),
        ),
    ]