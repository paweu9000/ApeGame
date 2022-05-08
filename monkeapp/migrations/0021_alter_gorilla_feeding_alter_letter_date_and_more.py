# Generated by Django 4.0.3 on 2022-05-08 10:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('monkeapp', '0020_opponent_look_alter_gorilla_feeding_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gorilla',
            name='feeding',
            field=models.DateField(default=datetime.datetime(2022, 5, 7, 10, 41, 11, 603609, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='letter',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 8, 10, 41, 11, 605603, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='opponent',
            name='look',
            field=models.ImageField(default='lion1', upload_to=''),
        ),
        migrations.AlterField(
            model_name='trainingtimer',
            name='finished_training',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 8, 12, 56, 11, 604606, tzinfo=utc)),
        ),
    ]
