# Generated by Django 2.2.6 on 2019-10-29 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writtenaudio', '0014_auto_20191027_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ttsservice',
            name='accent',
            field=models.CharField(default='', max_length=35),
        ),
    ]
