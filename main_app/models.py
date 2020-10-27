from djongo import models
from django.contrib.auth.models import User
import datetime
import django.utils

# Create your models here.

class Location(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    long = models.DecimalField(decimal_places=9, max_digits=20)
    lat = models.DecimalField(decimal_places=9, max_digits=20)

class Map(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    locations = models.ArrayReferenceField(
        to=Location,
        on_delete=models.CASCADE,
    )

# Profile Model
class Profile(models.Model):
    join_date = models.DateField(default=django.utils.timezone.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    maps = models.ArrayReferenceField(
        to=Map,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username


