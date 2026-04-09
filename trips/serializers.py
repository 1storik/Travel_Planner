from rest_framework import serializers
from .models import TravelProject, ProjectPlace
from .services import ArtInstituteService


class ProjectPlaceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ['id', 'external_id', 'title', 'notes', 'visited']


class ProjectPlaceCreateSerializer(serializers.Serializer):
    external_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        project = self.context.get('project')
        external_id = attrs['external_id']

        if project is not None:
            if project.places.count() >= 10:
                raise serializers.ValidationError("A project cannot contain more than 10 places.")

            if project.places.filter(external_id=external_id).exists():
                raise serializers.ValidationError("This place is already added to the project.")

        artwork = ArtInstituteService.get_artwork(external_id)
        if not artwork:
            raise serializers.ValidationError("Artwork not found in Art Institute API.")

        attrs['artwork'] = artwork
        return attrs

    def create(self, validated_data):
        project = self.context['project']
        artwork = validated_data['artwork']

        return ProjectPlace.objects.create(
            project=project,
            external_id=artwork['id'],
            title=artwork.get('title'),
            notes=validated_data.get('notes'),
        )


class ProjectPlaceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ['notes', 'visited']


class TravelProjectCreateSerializer(serializers.ModelSerializer):
    places = ProjectPlaceCreateSerializer(many=True, required=False)

    class Meta:
        model = TravelProject
        fields = ['id', 'name', 'description', 'start_date', 'places']

    def validate_places(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("A project cannot contain more than 10 places.")

        external_ids = [item['external_id'] for item in value]
        if len(external_ids) != len(set(external_ids)):
            raise serializers.ValidationError("Duplicate places are not allowed in the same project.")

        return value

    def create(self, validated_data):
        places_data = validated_data.pop('places', [])
        project = TravelProject.objects.create(**validated_data)

        created_places = []

        try:
            for place_data in places_data:
                artwork = ArtInstituteService.get_artwork(place_data['external_id'])
                if not artwork:
                    raise serializers.ValidationError(
                        {"places": f"Artwork with external_id={place_data['external_id']} was not found."}
                    )

                created_places.append(
                    ProjectPlace(
                        project=project,
                        external_id=artwork['id'],
                        title=artwork.get('title'),
                        notes=place_data.get('notes'),
                    )
                )

            if created_places:
                ProjectPlace.objects.bulk_create(created_places)

            return project
        except Exception:
            project.delete()
            raise


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