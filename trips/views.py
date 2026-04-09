from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import TravelProject, ProjectPlace
from .serializers import (
    TravelProjectCreateSerializer,
    TravelProjectUpdateSerializer,
    TravelProjectReadSerializer,
    ProjectPlaceCreateSerializer,
    ProjectPlaceReadSerializer,
    ProjectPlaceUpdateSerializer,
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


class ProjectPlaceListCreateView(generics.ListCreateAPIView):
    def get_project(self):
        return get_object_or_404(TravelProject, pk=self.kwargs['project_id'])

    def get_queryset(self):
        project = self.get_project()
        return project.places.all().order_by('id')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectPlaceCreateSerializer
        return ProjectPlaceReadSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = self.get_project()
        return context


class ProjectPlaceDetailView(generics.RetrieveUpdateAPIView):
    def get_project(self):
        return get_object_or_404(TravelProject, pk=self.kwargs['project_id'])

    def get_object(self):
        project = self.get_project()
        return get_object_or_404(
            ProjectPlace,
            pk=self.kwargs['place_id'],
            project=project
        )

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProjectPlaceUpdateSerializer
        return ProjectPlaceReadSerializer