from django.shortcuts import render
from .serializers import VideoLessons
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import VideoLesson


class VideoLessonView(APIView):

    def get(self, request):
        return Response(data=VideoLessons(VideoLesson.objects.all(), many=True).data)
