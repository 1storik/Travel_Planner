from django.urls import path
from .views import TravelProjectListCreateView, TravelProjectDetailView

urlpatterns = [
    path('projects/', TravelProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', TravelProjectDetailView.as_view(), name='project-detail'),
]