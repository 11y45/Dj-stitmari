from django.db import models
from django.urls import reverse
import uuid


class Project(models.Model):
    # General information about the project
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # new
    name = models.CharField(max_length=255)
    manager = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    profit = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    updates = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date_inv = models.DateField()
    Holding_periode = models.IntegerField()
    end_date_prj = models.DateField()
    is_completed = models.BooleanField(default=False)

    # MoneyField
    total_amount = models.IntegerField()
    min_investment = models.IntegerField(default=100)
    coverage_percentage = models.IntegerField(default=0)
    location = models.CharField(max_length=255)

    # Location fields
    map_center = models.JSONField(
        default=dict
    )  # For storing map center {latitude: ..., longitude: ...}
    polygon_corners = models.JSONField(
        default=list, blank=True, null=True
    )  # For storing a list of corners

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_index"),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # new
        return reverse("project_detail", args=[str(self.id)])


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="img/", blank=True)

    def __str__(self):
        return f"{self.project.name} Image"


class ProjectDocument(models.Model):
    project = models.ForeignKey(
        Project, related_name="documents", on_delete=models.CASCADE
    )
    document = models.FileField(upload_to="file/", blank=True)

    def __str__(self):
        return f"{self.project.name} file"
