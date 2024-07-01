from django.shortcuts import render
from transactions.models import BankTransaction, Account
from django.http import HttpResponse

def index(request):
    context = {
        "greeting": "Hello, world!",
    }
    return render(request, "transactions/index.html", context)


def get_bank_transactions(request):
    try:
        accounts = Account.objects.all()
        transactions = []
        for transaction in BankTransaction.objects.all():
            transactions.append({
                "date": transaction.date,
                "description": transaction.description,
                "amount": transaction.amount,
                "bank_balance": transaction.bank_balance,
            })

        context = {
            "accounts": accounts,
            "transactions": transactions,
        }

        return render(request, "transactions/bank_transactions.html", context)
    except ValueError as e:
        return HttpResponse(f"ValueError: {e}")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
