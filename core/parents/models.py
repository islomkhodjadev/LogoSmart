from django.db import models
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model


class City(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=200, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="regions")

    def __str__(self):
        return self.name


class Parent(models.Model):

    paid = models.BooleanField(default=False, blank=True)
    user = models.OneToOneField(
        get_user_model(), related_name="parent", on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    age = models.IntegerField()

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="parent")
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="parent", null=True, blank=True
    )

    def __str__(self):
        return self.name


class Child(models.Model):

    class Gender(models.TextChoices):
        male = "M", "MALE"
        female = "F", "FEMALE"

    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.male)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    image = models.ImageField(upload_to="parents/child/")

    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="child")

    def __str__(self):
        return self.name


from levels.models import Level


class ChildLevels(models.Model):
    child = models.ForeignKey(
        Child, on_delete=models.CASCADE, related_name="childlevels"
    )
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="childlevels"
    )
    
    stars = models.IntegerField(choices=((1, "bronze"), (2, "silver"), (3, "gold")))
    complete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """ensures that first element is latest created level"""

        ordering = ["-created_at"]
        unique_together = ("child", "level")
