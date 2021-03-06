# Generated by Django 3.2.8 on 2021-11-16 20:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/users/avatars/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bookmarked_by',
            field=models.ManyToManyField(blank=True, related_name='_users_user_bookmarked_by_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='cover_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/users/covers/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='_users_user_liked_by_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='province',
            field=models.CharField(blank=True, choices=[(1, 'آذربایجان شرقی'), (2, 'آذربایجان غربی'), (3, 'اردبیل'), (4, 'اصفهان'), (5, 'البرز'), (6, 'ایلام'), (7, 'بوشهر'), (8, 'تهران'), (9, 'چهارمحال و بختیاری'), (10, 'خراسان جنوبی'), (11, 'خراسان رضوی'), (12, 'خراسان شمالی'), (13, 'خوزستان'), (14, 'زنجان'), (15, 'سمنان'), (16, 'سیستان و بلوچستان'), (17, 'فارس'), (18, 'قزوین'), (19, 'قم'), (20, 'کردستان'), (21, 'کرمان'), (22, 'کرمانشاه'), (23, 'کهگیلویه و بویراحمد'), (24, 'گلستان'), (25, 'لرستان'), (26, 'گیلان'), (27, 'مازندران'), (28, 'مرکزی'), (29, 'هرمزگان'), (30, 'همدان'), (31, 'یزد')], max_length=30, null=True),
        ),
    ]
