from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Gorilla(models.Model):
    name = models.CharField(max_length=30)
    level = models.IntegerField(default=1)
    strength = models.IntegerField(default=5)
    hp = models.IntegerField(default=100)
    pvp_points = models.IntegerField(default=0)
    feeding = models.DateField(default=timezone.now() - timedelta(days=1))
    look = models.ImageField(default='default.png')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Equipment(models.Model):
    item1 = models.IntegerField(default=0)
    item2 = models.IntegerField(default=0)
    item3 = models.IntegerField(default=0)
    item4 = models.IntegerField(default=0)
    item5 = models.IntegerField(default=0)
    gold = models.IntegerField(default=500)
    golden_banana = models.IntegerField(default=0)
    equipment_owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Opponent(models.Model):
    name = models.CharField(default='xyz', max_length=100)
    strength = models.IntegerField(default=3)
    look = models.ImageField(default='lion1.png')
    health_points = models.IntegerField(default=50)

class TrainingTimer(models.Model):
    trained_gorilla = models.ForeignKey(Gorilla, on_delete=models.CASCADE)
    started_training = models.DateTimeField(auto_now=True)
    finished_training = models.DateTimeField(default=timezone.now() + timedelta(minutes=135))

class Auction(models.Model):
    item = models.CharField(max_length=30)
    amount_of_items = models.IntegerField()
    cost = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class Profile(models.Model):
    information = models.CharField(max_length=5000, default=None, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Letter(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    title = models.CharField(null=False, max_length=50)
    content = models.CharField(null=False, max_length=3000)
    date = models.DateTimeField(default=timezone.now())
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")





