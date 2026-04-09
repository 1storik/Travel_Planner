from rest_framework import serializers
from .models import TravelProject, ProjectPlace


class ProjectPlaceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ['id', 'external_id', 'title', 'notes', 'visited']


class TravelProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelProject
        fields = ['id', 'name', 'description', 'start_date']


class TravelProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelProject
        fields = ['name', 'description', 'start_date']


class TravelProjectReadSerializer(serializers.ModelSerializer):
    places = ProjectPlaceReadSerializer(many=True, read_only=True)
    is_completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = TravelProject
        fields = [
            'id',
            'name',
            'description',
            'start_date',
            'is_completed',
            'places',
            'created_at',
            'updated_at',
        ]
