# Generated by Django 2.2.6 on 2019-10-13 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('writtenaudio', '0004_auto_20191013_1353'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='track',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='tracktext',
            options={'ordering': ['time_marker']},
        ),
    ]
