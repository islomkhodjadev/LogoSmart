from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import TrainingMainCategory
from .serializers import TrainingMainCategorySerializer


class TrainingMainCategoryListView(generics.ListAPIView):
    queryset = TrainingMainCategory.objects.all()
    serializer_class = TrainingMainCategorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
