from rest_framework import generics, status
from rest_framework.response import Response
from .models import TravelProject
from .serializers import (
    TravelProjectCreateSerializer,
    TravelProjectUpdateSerializer,
    TravelProjectReadSerializer,
)


class TravelProjectListCreateView(generics.ListCreateAPIView):
    queryset = TravelProject.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TravelProjectCreateSerializer
        return TravelProjectReadSerializer


class TravelProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TravelProject.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TravelProjectUpdateSerializer
        return TravelProjectReadSerializer

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        if project.places.filter(visited=True).exists():
            return Response(
                {"detail": "Project cannot be deleted because it contains visited places."},
                status=status.HTTP_409_CONFLICT
            )

        self.perform_destroy(project)
        return Response(status=status.HTTP_204_NO_CONTENT)
