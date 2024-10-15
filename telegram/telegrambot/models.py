from django.db import models

# Create your models here.


class Bola(models.Model):
    firstName = models.CharField(max_length=200)
    LastName = models.CharField(max_length=200)
    year = models.IntegerField()
    token = models.CharField(max_length=300, unique=True)
    