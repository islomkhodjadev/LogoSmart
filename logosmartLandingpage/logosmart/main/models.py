from django.db import models

# Create your models here.


class Comments(models.Model):
    fullName = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.comment

class Question(models.Model):
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question

class Savollar(models.Model):
    savol = models.CharField(max_length=200)

    def __str__(self):
        return self.savol







class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="answer")
    answer = models.CharField(max_length=200)
    def __str__(self):
        return self.answer
    