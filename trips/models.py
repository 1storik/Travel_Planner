from django.db import models


class TravelProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_completed(self):
        places = self.places.all()
        return places.exists() and not places.filter(visited=False).exists()

    def __str__(self):
        return self.name


class ProjectPlace(models.Model):
    project = models.ForeignKey(
        TravelProject,
        on_delete=models.CASCADE,
        related_name='places'
    )
    external_id = models.IntegerField()
    title = models.CharField(max_length=500, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    visited = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'external_id'],
                name='unique_project_external_place'
            )
        ]

    def __str__(self):
        return f'{self.project.name}: {self.external_id}'
