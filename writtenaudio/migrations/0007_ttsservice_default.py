# Generated by Django 2.2.6 on 2019-10-21 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writtenaudio', '0006_auto_20191021_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='ttsservice',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
