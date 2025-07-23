from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from wallet.models import Wallet
from django.db import models
from datetime import date


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    def wallet_balance(self, obj):
        try:
            return obj.wallet.balance
        except Wallet.DoesNotExist:
            return "No wallet"

    list_display = [
        "email",
        "phone",
        "city",
        "birth_date",
        "is_staff",
        "wallet_balance",
    ]

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "phone",
                    "city",
                    "birth_date",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "phone",
                    "city",
                    "birth_date",
                )
            },
        ),
    )

    change_list_template = "admin/user_charts.html"

    def changelist_view(self, request, extra_context=None):
        # Add your data processing and chart context here
        extra_context = extra_context or {}

        # Example: Adding some context for charts
        extra_context["chart_data"] = self.get_chart_data()

        return super().changelist_view(request, extra_context=extra_context)

    def get_chart_data(self):
        # City Chart Data
        users_per_city = CustomUser.objects.values("city").annotate(
            count=models.Count("id")
        )
        city_chart_labels = [item["city"] for item in users_per_city]
        city_chart_values = [item["count"] for item in users_per_city]

        # Age Category Data
        today = date.today()
        age_categories = {"18-25": 0, "25-35": 0, "35-45": 0, "45-55": 0, "55+": 0}

        for user in CustomUser.objects.exclude(birth_date__isnull=True):
            age = (
                today.year
                - user.birth_date.year
                - (
                    (today.month, today.day)
                    < (user.birth_date.month, user.birth_date.day)
                )
            )

            if 18 <= age <= 25:
                age_categories["18-25"] += 1
            elif 25 < age <= 35:
                age_categories["25-35"] += 1
            elif 35 < age <= 45:
                age_categories["35-45"] += 1
            elif 45 < age <= 55:
                age_categories["45-55"] += 1
            elif age > 55:
                age_categories["55+"] += 1

        age_chart_labels = list(age_categories.keys())
        age_chart_values = list(age_categories.values())

        return {
            "city_chart_labels": city_chart_labels,
            "city_chart_values": city_chart_values,
            "age_chart_labels": age_chart_labels,
            "age_chart_values": age_chart_values,
        }


admin.site.register(CustomUser, CustomUserAdmin)
