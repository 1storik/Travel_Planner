from django.urls import path
from .views import (
    TravelProjectListCreateView,
    TravelProjectDetailView,
    ProjectPlaceListCreateView,
    ProjectPlaceDetailView,
)

urlpatterns = [
    path('projects/', TravelProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', TravelProjectDetailView.as_view(), name='project-detail'),

    path('projects/<int:project_id>/places/', ProjectPlaceListCreateView.as_view(), name='project-place-list-create'),
    path('projects/<int:project_id>/places/<int:place_id>/', ProjectPlaceDetailView.as_view(), name='project-place-detail'),
]
