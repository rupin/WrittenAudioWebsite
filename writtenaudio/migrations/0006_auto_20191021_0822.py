# Generated by Django 2.2.6 on 2019-10-21 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('writtenaudio', '0005_ttsservice_premium_voice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='output_format',
        ),
        migrations.AddField(
            model_name='track',
            name='podcast_mode',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='track',
            name='voice_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='writtenaudio.TTSService'),
        ),
        migrations.AddField(
            model_name='ttsservice',
            name='cost',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='ttsservice',
            name='enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='track',
            name='audio_file',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]
