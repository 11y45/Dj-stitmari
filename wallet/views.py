from django.shortcuts import render
from .models import Wallet, NormTransaction, InvTransaction
from project.models import Project
from .forms import InvestmentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView, FormView, CreateView
from .forms import DepositForm, WithdrawalForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Sum
from django.db.models.functions import TruncDay
import json


class WalletDetailView(LoginRequiredMixin, DetailView):
    model = Wallet
    template_name = "wallet/wallet_detail.html"
    context_object_name = "wallet"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        norm_transactions = NormTransaction.objects.filter(wallet=self.object)
        inv_transactions = InvTransaction.objects.filter(wallet=self.object)

        # Combine and order by time
        context["transactions"] = sorted(
            list(norm_transactions) + list(inv_transactions),
            key=lambda t: t.time,
            reverse=True,
        )
        context["inv_transactions"] = sorted(
            inv_transactions, key=lambda t: t.time, reverse=True
        )

        # Data for Investment Chart
        investment_data = inv_transactions.values("project__type").annotate(
            total=Sum("amount")
        )
        context["investment_chart_data"] = json.dumps(
            {
                "labels": [item["project__type"] for item in investment_data],
                "data": [float(item["total"]) for item in investment_data],
            }
        )

        # Data for Transaction History Chart (Daily)
        deposit_data = (
            norm_transactions.filter(transaction_type="deposit")
            .annotate(day=TruncDay("time"))
            .values("day")
            .annotate(total=Sum("amount"))
        )
        withdrawal_data = (
            norm_transactions.filter(transaction_type="withdrawal")
            .annotate(day=TruncDay("time"))
            .values("day")
            .annotate(total=Sum("amount"))
        )

        context["transaction_chart_data"] = json.dumps(
            {
                "labels": [item["day"].strftime("%Y-%m-%d") for item in deposit_data],
                "deposits": [float(item["total"]) for item in deposit_data],
                "withdrawals": [float(item["total"]) for item in withdrawal_data],
            }
        )

        return context

    def get_object(self, queryset=None):
        return Wallet.objects.get(user=self.request.user)


class CashPlusView(LoginRequiredMixin, TemplateView):
    template_name = "wallet/cashplus.html"


class DepositFundsView(LoginRequiredMixin, FormView):
    template_name = "wallet/deposit_funds.html"
    form_class = DepositForm
    success_url = reverse_lazy("wallet")

    def form_valid(self, form):
        amount = form.cleaned_data["amount"]
        wallet = self.request.user.wallet
        wallet.balance += amount
        wallet.save()

        NormTransaction.objects.create(
            wallet=wallet,
            transaction_type="deposit",
            amount=amount,
        )
        # Add a custom tag 'transaction' to this message
        messages.success(
            self.request,
            f"Successfully deposited {amount} to your wallet.",
            extra_tags="transaction",
        )
        return super().form_valid(form)


class WithdrawFundsView(LoginRequiredMixin, FormView):
    template_name = "wallet/withdraw_funds.html"
    form_class = WithdrawalForm
    success_url = reverse_lazy("wallet")

    def form_valid(self, form):
        amount = form.cleaned_data["amount"]
        wallet = self.request.user.wallet
        if amount > wallet.balance:
            # Add a custom tag 'transaction' to this message
            messages.error(
                self.request, "Insufficient funds!", extra_tags="transaction"
            )
            return redirect("withdraw_funds")
        else:
            wallet.balance -= amount
            wallet.save()

            NormTransaction.objects.create(
                wallet=wallet,
                transaction_type="withdrawal",
                amount=amount,
            )
            # Add a custom tag 'transaction' to this message
            messages.success(
                self.request,
                f"Successfully withdrew {amount} from your wallet.",
                extra_tags="transaction",
            )
            return super().form_valid(form)


class InvestmentView(LoginRequiredMixin, FormView):
    form_class = InvestmentForm
    template_name = "wallet/investment.html"
    success_url = reverse_lazy("wallet")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs["pk"]
        project = get_object_or_404(Project, id=project_id)
        wallet = get_object_or_404(Wallet, user=self.request.user)

        # Calculate the total invested amount so far
        total_invested = sum(
            transaction.amount for transaction in project.investment_transactions.all()
        )

        # Calculate how much can still be invested
        remaining_investable_amount = project.total_amount - total_invested

        # Pass necessary context to the template
        context["project"] = project
        context["wallet"] = wallet
        context["remaining_investable_amount"] = remaining_investable_amount

        return context

    def form_valid(self, form):
        project_id = self.kwargs["pk"]
        project = get_object_or_404(Project, id=project_id)
        wallet = get_object_or_404(Wallet, user=self.request.user)

        amount = form.cleaned_data["amount"]

        # Custom validation logic
        if amount <= 0:
            form.add_error("amount", "Invalid amount.")
            return self.form_invalid(form)
        if amount > project.total_amount:
            form.add_error(
                "amount", "Amount cannot be greater than the project's total amount."
            )
            return self.form_invalid(form)
        if amount < project.min_investment:
            form.add_error(
                "amount", "Amount cannot be smaller than the minimum investment."
            )
            return self.form_invalid(form)

        if wallet.balance < amount:
            form.add_error("amount", "Insufficient balance.")
            return self.form_invalid(form)

        # Calculate the total invested amount so far
        total_invested = sum(
            transaction.amount for transaction in project.investment_transactions.all()
        )

        # Calculate how much can still be invested
        remaining_investable_amount = project.total_amount - total_invested

        # Check if the investment amount exceeds the remaining investable amount
        if amount > remaining_investable_amount:
            form.add_error(
                "amount",
                f"This investment would exceed the project's total required amount. "
                f"You can only invest up to {remaining_investable_amount}.",
            )
            return self.form_invalid(form)

        # If validation passes, update the wallet and create the transaction
        wallet.balance -= amount
        wallet.save()

        # Create and save the investment transaction
        InvTransaction.objects.create(project=project, wallet=wallet, amount=amount)

        # Add a success message
        messages.success(
            self.request,
            f"Successfully Invested {amount} in {project.name}.",
            extra_tags="transaction",
        )

        # Return the form valid response (which by default redirects to success_url)
        return super().form_valid(form)
