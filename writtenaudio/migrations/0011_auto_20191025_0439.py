# Generated by Django 2.2.6 on 2019-10-25 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('writtenaudio', '0010_track_file_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ttsservice',
            options={'ordering': ['name', 'accent'], 'verbose_name': 'TTS Service'},
        ),
    ]