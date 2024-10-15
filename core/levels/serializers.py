from rest_framework import serializers
from .models import TrainingMainCategory, Level, Images


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ["image"]


class LevelSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)  # Use the ImageSerializer here

    class Meta:
        model = Level
        fields = ["id", "category", "text", "voice", "images"]


class TrainingMainCategorySerializer(serializers.ModelSerializer):
    level = LevelSerializer(many=True, read_only=True)

    class Meta:
        model = TrainingMainCategory
        fields = ["id", "name", "age_min", "age_max", "level"]
