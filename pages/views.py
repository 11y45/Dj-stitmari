from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class FaqPageView(TemplateView):
    template_name = "pages/faq.html"


class AboutPageView(TemplateView):  # new
    template_name = "pages/about.html"
