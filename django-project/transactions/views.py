from django.shortcuts import render
from transactions.models import BankTransaction


def index(request):
    context = {
        "greeting": "Hello, world!",
    }
    return render(request, "transactions/index.html", context)


def get_bank_transactions(request):
    transactions = []
    for transaction in BankTransaction.objects.all():
        transactions.append({
            "date": transaction.date,
            "description": transaction.description,
            "amount": transaction.amount,
            "bank_balance": transaction.bank_balance,
        })

    context = {
        "transactions": transactions,
    }

    return render(request, "transactions/bank_transactions.html", context)