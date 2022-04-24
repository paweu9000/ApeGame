from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Gorilla(models.Model):
    name = models.CharField(max_length=30)
    level = models.IntegerField(default=1)
    strength = models.IntegerField(default=5)
    hp = models.IntegerField(default=100)
    skill_points = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Equipment(models.Model):
    item1 = models.IntegerField(default=0)
    item2 = models.IntegerField(default=0)
    item3 = models.IntegerField(default=0)
    item4 = models.IntegerField(default=0)
    item5 = models.IntegerField(default=0)
    equipment_owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Opponent(models.Model):
    name = models.CharField(default='George Floyd', max_length=100)
    strength = models.IntegerField(default=3)
    health_points = models.IntegerField(default=50)

class TrainingTimeEvent(models.Model):
    name = models.CharField(max_length=200)
    when = models.DateField()

    def __str__(self):
        return self.name




