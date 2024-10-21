from django.shortcuts import render
from .models import Comments, Question, Answer, Savollar
# Create your views here.


def index(request):

    data = {
    "questions" : Question.objects.all(),
    "comments": Comments.objects.all(),
        "question_count": Question.objects.count()
    }
    if request.method == "POST":
        savol = request.POST.get("savol", None)
        print(savol)
        if savol and len(savol) < 200:
            Savollar.objects.create(savol=savol)

    return render(request, "index.html", context=data)