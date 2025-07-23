from django.urls import path, include
from .views import (
    ProjectListView,
    ProjectdetailView,
)

urlpatterns = [
    path("", ProjectListView.as_view(), name="home"),
    path("<uuid:pk>", ProjectdetailView.as_view(), name="project_detail"),
]
