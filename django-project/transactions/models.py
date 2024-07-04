from django.db import models
import uuid


def get_default_debit_account():
    return Account.objects.get(name='Misc').id


def get_default_credit_account():
    return Account.objects.get(name="Cash at bank").id

def get_default_debit_entry():
    return AccountingEntry.objects.get(type='Debit').id

def get_default_credit_entry():
    return AccountingEntry.objects.get(type='Credit').id


class AccountingEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bank_transaction = models.ForeignKey('BankTransaction', on_delete=models.CASCADE, default=1)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, default=1)
    date = models.DateField()
    type = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    keywords = models.JSONField()
    budget_category = models.ForeignKey('BudgetSuperCategory', on_delete=models.CASCADE, default='Needs')

    def __str__(self):
        return self.name


class AccountingTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    debit_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accounting_transaction_debit_account', default=get_default_debit_account)
    credit_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accounting_transaction_credit_account', default=get_default_credit_account)
    debit_entry = models.ForeignKey(AccountingEntry, on_delete=models.CASCADE, related_name='debit_entry', default=get_default_debit_entry)
    credit_entry = models.ForeignKey(AccountingEntry, on_delete=models.CASCADE, related_name='credit_entry', default=get_default_credit_entry)

    def __str__(self):
        return self.description


class BankTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    bank_balance = models.DecimalField(max_digits=10, decimal_places=2)
    tokens = models.JSONField(default=dict)
    debit_account = models.ForeignKey(Account, on_delete=models.SET_DEFAULT, related_name="bank_transaction_debit_account",
                                      default=get_default_debit_account)
    credit_account = models.ForeignKey(Account, on_delete=models.SET_DEFAULT, related_name="bank_transaction_credit_account",
                                       default=get_default_credit_account)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'amount', 'description', 'bank_balance'],
                name='unique_bank_transaction'
            )
        ]

    def __str__(self):
        return self.description


class BudgetSuperCategory(models.Model):
    """
    This model is used to group budget categories into super categories such as 'Needs', 'Wants', 'Savings', etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

