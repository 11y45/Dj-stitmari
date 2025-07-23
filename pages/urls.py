from django.urls import path
from .views import FaqPageView, AboutPageView

urlpatterns = [
    path("faq/", FaqPageView.as_view(), name="faq"),
    path("about/", AboutPageView.as_view(), name="about"),  # new
]
