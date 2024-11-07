# Generated by Django 5.1.2 on 2024-10-30 20:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0005_alter_image_image_file_friend'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=models.ImageField(upload_to='profile_images/'),
        ),
        migrations.AlterField(
            model_name='statusmessage',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_fb.profile'),
        ),
    ]