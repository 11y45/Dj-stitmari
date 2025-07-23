from django.db import models
from accounts.models import CustomUser
from project.models import Project
from django.utils import timezone

# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"


class NormTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
    )

    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    time = models.DateTimeField(default=timezone.now)


class InvTransaction(models.Model):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="investment_transactions"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="investment_transactions"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    time = models.DateTimeField(default=timezone.now)

    # Overide the save transaction
    def save(self, *args, **kwargs):
        # Save the transaction
        super().save(*args, **kwargs)

        # Update the project's coverage percentage and completion status
        total_invested = sum(
            transaction.amount
            for transaction in self.project.investment_transactions.all()
        )
        coverage_percentage = (total_invested / self.project.total_amount) * 100
        self.project.coverage_percentage = coverage_percentage

        # Mark the project as completed if coverage percentage reaches 100%
        if coverage_percentage >= 100:
            self.project.is_completed = True
        else:
            self.project.is_completed = False
        self.project.save()
