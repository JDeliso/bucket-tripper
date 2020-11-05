from django.db import models
from django.contrib.auth.models import User

import datetime
import django.utils

# Create your models here.
# Profile Model
class Profile(models.Model):
    join_date = models.DateField(default=django.utils.timezone.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

class Map(models.Model):
    name = models.CharField(max_length=100, default="default")
    description = models.TextField(max_length=5000, default="Your first map!")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    long = models.DecimalField(decimal_places=50, max_digits=60)
    lat = models.DecimalField(decimal_places=50, max_digits=60)
    map_id = models.ForeignKey(Map, on_delete=models.CASCADE)





