from django.contrib import admin
from .models import Project, ProjectDocument, ProjectImage


# Register your models here.


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 0  #


class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 0  #


class ProjectAdmin(admin.ModelAdmin):

    inlines = [ProjectImageInline, ProjectDocumentInline]

    list_display = (
        "name",
        "manager",
        "total_amount",
        "created_at",
        "coverage_percentage",
        "is_completed",
    )


admin.site.register(Project, ProjectAdmin)
