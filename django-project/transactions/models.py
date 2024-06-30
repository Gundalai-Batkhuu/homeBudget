from django.db import models
import uuid

class AccountingEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    entries = models.ManyToManyField(AccountingEntry)
    type = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    keywords = models.JSONField()

    def __str__(self):
        return self.name


class AccountingTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_account')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_account')
    transaction_type = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class BankTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    bank_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'amount', 'description', 'bank_balance'],
                name='unique_bank_transaction'
            )
        ]

    def __str__(self):
        return self.description