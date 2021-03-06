# Generated by Django 2.2.6 on 2019-10-25 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('writtenaudio', '0011_auto_20191025_0439'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVoiceProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_default_profile', models.BooleanField(default=False)),
                ('enabled', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('voice_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='writtenaudio.TTSService')),
            ],
            options={
                'verbose_name': 'User Voice Profile',
            },
        ),
    ]
