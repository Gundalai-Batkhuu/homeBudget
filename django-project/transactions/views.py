from django.shortcuts import render, redirect
from transactions.models import BankTransaction, Account
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
import json
from django.core.paginator import Paginator


def index(request):
    context = {
        "greeting": "Hello, world!",
    }
    return render(request, "transactions/index.html", context)


def get_bank_transactions(request):
    try:
        accounts = Account.objects.all()
        transactions = BankTransaction.objects.all()

        paginator = Paginator(transactions, 9)  # Show 10 transactions per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            "accounts": accounts,
            "page_obj": page_obj,
        }

        return render(request, "transactions/bank_transactions.html", context)
    except ValueError as e:
        return HttpResponse(f"ValueError: {e}")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


import logging

logger = logging.getLogger(__name__)

@csrf_protect
def update_debit_account(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        account_name = request.POST.get('account_name')

        try:
            transaction = BankTransaction.objects.get(id=transaction_id)
            account = Account.objects.get(name=account_name)
            transaction.debit_account = account
            transaction.save()
            # Redirect to the same page after updating
            return redirect(request.META.get('HTTP_REFERER'))
        except (BankTransaction.DoesNotExist, Account.DoesNotExist) as e:
            # Handle the error accordingly
            print(f'Error updating transaction: {e}')
            # Redirect back with an error message or render a specific error template
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('transaction_list')  # Default redirect if not POST request

