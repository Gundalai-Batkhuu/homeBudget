import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from transactions.models import BankTransaction, AccountingEntry, Account, AccountingTransaction, BudgetSuperCategory


def add_accounting_transactions():
    bank_transactions = BankTransaction.objects.all()
    for transaction in bank_transactions:
        debit_entry = AccountingEntry(
            bank_transaction=transaction,
            account=transaction.debit_account,
            date=transaction.date,
            type='Debit',
            amount=abs(transaction.amount),
            description=transaction.description
        )
        credit_entry = AccountingEntry(
            bank_transaction=transaction,
            account=transaction.credit_account,
            date=transaction.date,
            type='Credit',
            amount=abs(transaction.amount),
            description=transaction.description
        )
        debit_entry.save()
        credit_entry.save()

        accounting_transaction = AccountingTransaction(
            date=transaction.date,
            amount=abs(transaction.amount),
            description=transaction.description,
            debit_account=transaction.debit_account,
            credit_account=transaction.credit_account,
            debit_entry=debit_entry,
            credit_entry=credit_entry
        )
        accounting_transaction.save()



