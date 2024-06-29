from django.db import models


class AccountingEntry(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class Account(models.Model):
    name = models.CharField(max_length=100)
    entries = models.ManyToManyField(AccountingEntry)
    type = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    keywords = models.JSONField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_account')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_account')
    transaction_type = models.CharField(max_length=100)

    def __str__(self):
        return self.description
