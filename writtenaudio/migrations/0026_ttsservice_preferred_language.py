# Generated by Django 2.2.6 on 2019-11-20 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writtenaudio', '0025_auto_20191118_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='ttsservice',
            name='preferred_language',
            field=models.ManyToManyField(to='writtenaudio.Language'),
        ),
    ]
