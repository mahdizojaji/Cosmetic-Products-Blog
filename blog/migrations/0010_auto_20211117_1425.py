# Generated by Django 3.2.8 on 2021-11-17 14:25

import blog.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import extensions.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('blog', '0009_alter_article_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='rate',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
        migrations.AddField(
            model_name='article',
            name='rate_counts',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='rate_points',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='article_bookmarks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='article_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='article',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID'),
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('object_id', models.PositiveIntegerField()),
                ('file', models.FileField(upload_to=blog.models.path_and_rename, verbose_name='File')),
                ('field_name', models.IntegerField(choices=[(0, 'Images'), (1, 'Videos'), (2, 'Sessions')], verbose_name='Field Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='media_files', to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ['course', 'article']}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, unique=True, verbose_name='Slug')),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Pending'), (2, 'Published')], default=0)),
                ('content', models.TextField(blank=True, null=True, verbose_name='Content')),
                ('cost', models.PositiveIntegerField(default=0, verbose_name='Cost')),
                ('is_online', models.BooleanField(verbose_name='Is Online')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantity')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('deadline', models.DateTimeField(blank=True, null=True, validators=[extensions.validators.FutureDateValidator()], verbose_name='Deadline')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
        ),
    ]