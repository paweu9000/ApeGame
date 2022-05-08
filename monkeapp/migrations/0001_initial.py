# Generated by Django 4.0.3 on 2022-04-30 13:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gorilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('level', models.IntegerField(default=1)),
                ('strength', models.IntegerField(default=5)),
                ('hp', models.IntegerField(default=100)),
                ('pvp_points', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Opponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='George Floyd', max_length=100)),
                ('strength', models.IntegerField(default=3)),
                ('health_points', models.IntegerField(default=50)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingTimer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_training', models.DateTimeField(auto_now=True)),
                ('finished_training', models.DateTimeField(default=datetime.datetime(2022, 4, 30, 15, 48, 45, 735809, tzinfo=utc))),
                ('trained_gorilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monkeapp.gorilla')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item1', models.IntegerField(default=0)),
                ('item2', models.IntegerField(default=0)),
                ('item3', models.IntegerField(default=0)),
                ('item4', models.IntegerField(default=0)),
                ('item5', models.IntegerField(default=0)),
                ('gold', models.IntegerField(default=500)),
                ('equipment_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=30)),
                ('amount_of_items', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]