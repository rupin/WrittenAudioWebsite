# Generated by Django 2.2.6 on 2019-10-31 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writtenaudio', '0016_track_audio_speed'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracktext',
            name='is_ssml',
            field=models.BooleanField(default=False),
        ),
    ]