from django.contrib import admin
from .models import Question, Comments, Answer, Savollar

# Register your models here.

admin.site.register(Question)
admin.site.register(Comments)
admin.site.register(Answer)
admin.site.register(Savollar)