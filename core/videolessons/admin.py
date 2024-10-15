from django.contrib import admin
from .models import VideoLesson

class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", 'video_url', 'description', "title")
    search_fields = ('title',)


admin.site.register(VideoLesson, VideoAdmin)
