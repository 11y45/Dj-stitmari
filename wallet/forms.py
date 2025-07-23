from django import forms
from project.models import Project


class DepositForm(forms.Form):
    amount = forms.IntegerField()

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount > 1000000:
            raise forms.ValidationError("Amount cannot be greater than 1,000,000.")
        return amount


class WithdrawalForm(forms.Form):
    amount = forms.IntegerField()


class InvestmentForm(forms.Form):
    amount = forms.IntegerField()
