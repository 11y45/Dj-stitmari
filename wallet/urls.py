from django.urls import path, include
from .views import (
    WalletDetailView,
    CashPlusView,
    DepositFundsView,
    WithdrawFundsView,
    InvestmentView,
)

urlpatterns = [
    path("", WalletDetailView.as_view(), name="wallet"),
    path("cashplus/", CashPlusView.as_view(), name="cashplus"),
    path("deposit/", DepositFundsView.as_view(), name="deposit_funds"),
    path("withdraw/", WithdrawFundsView.as_view(), name="withdraw_funds"),
    path("<uuid:pk>/", InvestmentView.as_view(), name="investment"),
]
