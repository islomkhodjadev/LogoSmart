from django.db import models
from django.core.exceptions import ValidationError


def validate_age_limit(value):
    if not (0 <= value <= 120):
        raise ValidationError(
            f"Age must be a realistic human age. You entered {value}."
        )


class TrainingMainCategory(models.Model):

    name = models.CharField(max_length=200, unique=True)
    age_min = models.IntegerField(validators=[validate_age_limit])
    age_max = models.IntegerField(validators=[validate_age_limit])

    def clean(self):

        if self.age_min >= self.age_max:
            raise ValidationError(
                {
                    "age_min": "Minimum age must be less than maximum age.",
                    "age_max": "Maximum age must be greater than minimum age.",
                }
            )

    class Meta:
        ordering = ["-id"]


class Images(models.Model):
    image = models.URLField(max_length=500)
    level = models.ForeignKey("Level", on_delete=models.CASCADE, related_name="images")


class Level(models.Model):
    paid = models.BooleanField(default=True)

    category = models.ForeignKey(
        TrainingMainCategory, on_delete=models.CASCADE, related_name="level"
    )
    text = models.CharField(max_length=100)
    voice = models.URLField(max_length=500)

    video = models.URLField(max_length=500)

    class Meta:
        ordering = ["-id"]
