from django.urls import path
from .views import VideoLessonView


urlpatterns = [
    path("", VideoLessonView.as_view())
]

