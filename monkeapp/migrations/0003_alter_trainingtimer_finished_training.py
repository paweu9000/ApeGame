# Generated by Django 4.0.3 on 2022-05-02 11:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('monkeapp', '0002_alter_trainingtimer_finished_training_usersettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingtimer',
            name='finished_training',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 2, 14, 13, 58, 320468, tzinfo=utc)),
        ),
    ]
