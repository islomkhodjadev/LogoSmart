from django.db import models

class VideoLesson(models.Model):

    video_url = models.URLField()
    description = models.TextField()
    title = models.CharField(max_length=200)

