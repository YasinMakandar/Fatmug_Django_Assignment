# Generated by Django 5.1.1 on 2024-09-15 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0002_video_subtitle_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='subtitles',
            field=models.TextField(blank=True),
        ),
    ]
