# Generated by Django 2.2.6 on 2019-11-20 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writtenaudio', '0026_ttsservice_preferred_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='system_default',
            field=models.BooleanField(default=False),
        ),
    ]
