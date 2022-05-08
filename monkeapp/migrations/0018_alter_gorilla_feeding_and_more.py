# Generated by Django 4.0.3 on 2022-05-08 09:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monkeapp', '0017_equipment_golden_banana_alter_gorilla_feeding_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gorilla',
            name='feeding',
            field=models.DateField(default=datetime.datetime(2022, 5, 7, 9, 35, 11, 68361, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='trainingtimer',
            name='finished_training',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 8, 11, 50, 11, 68361, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=3000)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
