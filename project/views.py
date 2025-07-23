from django.shortcuts import render
from .models import Project
from wallet.models import Wallet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404


# Create your views here.
class ProjectListView(ListView):
    model = Project
    # Zadha bach y3yt liha bsmya f html tags
    context_object_name = "project_list"
    template_name = "project/home.html"


class ProjectdetailView(LoginRequiredMixin, DetailView):
    model = Project
    # Zadha bach y3yt liha bsmya f html tags
    context_object_name = "project"
    template_name = "project/project_detail.html"
    # login_url for the user to be redirected to.
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure the user is authenticated before querying the Wallet
        if self.request.user.is_authenticated:
            wallet = get_object_or_404(Wallet, user=self.request.user)
            context["wallet"] = wallet
        return context
