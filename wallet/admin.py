from django.contrib import admin
from django.db.models import Sum
from .models import Wallet, NormTransaction, InvTransaction
from django.utils.dateformat import DateFormat


class WalletAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "balance",
    )
    change_list_template = "admin/wallet_charts.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Fetch data for the chart
        extra_context["chart_data"] = self.get_chart_data()
        return super().changelist_view(request, extra_context=extra_context)

    def get_chart_data(self):
        # Fetch investment transactions and aggregate by day
        investment_data = (
            InvTransaction.objects.values("time__date")
            .annotate(total=Sum("amount"))
            .order_by("time__date")
        )

        # Fetch deposit transactions and aggregate by day
        deposit_data = (
            NormTransaction.objects.filter(transaction_type="deposit")
            .values("time__date")
            .annotate(total=Sum("amount"))
            .order_by("time__date")
        )

        # Fetch withdrawal transactions and aggregate by day
        withdrawal_data = (
            NormTransaction.objects.filter(transaction_type="withdrawal")
            .values("time__date")
            .annotate(total=Sum("amount"))
            .order_by("time__date")
        )

        # Extract the days and total amounts
        days_investment = set(investment_data.values_list("time__date", flat=True))
        days_deposit = set(deposit_data.values_list("time__date", flat=True))
        days_withdrawal = set(withdrawal_data.values_list("time__date", flat=True))

        # Combine all unique dates from all three datasets
        all_days = sorted(days_investment | days_deposit | days_withdrawal)

        days = [DateFormat(day).format("Y-m-d") for day in all_days]

        totals_investment = []
        totals_deposit = []
        totals_withdrawal = []

        for day in all_days:
            totals_investment.append(
                float(
                    next(
                        (
                            item["total"]
                            for item in investment_data
                            if item["time__date"] == day
                        ),
                        0,
                    )
                )
            )
            totals_deposit.append(
                float(
                    next(
                        (
                            item["total"]
                            for item in deposit_data
                            if item["time__date"] == day
                        ),
                        0,
                    )
                )
            )
            totals_withdrawal.append(
                float(
                    next(
                        (
                            item["total"]
                            for item in withdrawal_data
                            if item["time__date"] == day
                        ),
                        0,
                    )
                )
            )

        chart_data = {
            "days": days,
            "totals_investment": totals_investment,
            "totals_deposit": totals_deposit,
            "totals_withdrawal": totals_withdrawal,
        }

        return chart_data


admin.site.register(Wallet, WalletAdmin)


class NormTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "amount",
        "transaction_type",
        "time",
    )


admin.site.register(NormTransaction, NormTransactionAdmin)


class InvTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "amount",
        "project",
        "time",
    )


admin.site.register(InvTransaction, InvTransactionAdmin)
