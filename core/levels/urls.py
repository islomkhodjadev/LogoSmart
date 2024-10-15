from django.urls import path

from .views import TrainingMainCategoryListView

urlpatterns = [path("", TrainingMainCategoryListView.as_view(), name="levels")]
