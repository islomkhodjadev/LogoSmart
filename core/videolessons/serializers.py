from rest_framework import serializers
from .models import VideoLesson

class VideoLessons(serializers.ModelSerializer):

    class Meta:
        model = VideoLesson
        fields = ("id", "video_url", "description", "title")
