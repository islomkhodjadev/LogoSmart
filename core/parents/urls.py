from django.urls import path
from .views import (
    ParentView,
    GetToken,
    ChildAPIView,
    Test,
    CityListView,
    ChildLevel,
    RegisterByPhone,
)


urlpatterns = [
    path("registerbyphone/", RegisterByPhone.as_view(), name="register-by-phone"),
    path(
        "registerbyphone/<str:phoneNumber>/",
        RegisterByPhone.as_view(),
        name="register-by-phone",
    ),
    path("authenticate/", GetToken.as_view(), name="token"),
    path("createparent/", ParentView.as_view(), name="createparent"),
    path("children/<int:pk>/", ChildAPIView.as_view(), name="child-detail"),
    path("childrencreate/", ChildAPIView.as_view(), name="child-create"),
    path("children/level/", ChildLevel.as_view(), name="child-level"),
    path("cities/", CityListView.as_view(), name="city-list"),
]
