# Generated by Django 2.2.6 on 2019-11-04 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writtenaudio', '0017_tracktext_is_ssml'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='audio_pitch',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]