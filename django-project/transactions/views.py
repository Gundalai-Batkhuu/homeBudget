import json
from decimal import Decimal
from transactions.models import BankTransaction, Account, AccountingTransaction, BudgetSuperCategory, AccountingEntry
from django.views.decorators.csrf import csrf_protect
from django.db.models import Sum
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from transactions.models import Account, AccountingTransaction
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse

from django.core.serializers.json import DjangoJSONEncoder
from transactions.util.bank_transactions import get_monthly_periods


def index(request):
    context = {
        "greeting": "Hello, world!",
    }
    return render(request, "transactions/index.html", context)


def get_bank_transactions(request):
    try:
        accounts = Account.objects.all()
        transactions = BankTransaction.objects.all().order_by('-date')

        paginator = Paginator(transactions, 20)
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


def get_misc_bank_transactions(request):
    try:
        accounts = Account.objects.all()
        transactions = BankTransaction.objects.filter(debit_account__name='Misc').order_by('-date')

        paginator = Paginator(transactions, 20)  # Show 10 transactions per page
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


@csrf_protect
def update_credit_account(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        account_name = request.POST.get('account_name')

        try:
            transaction = BankTransaction.objects.get(id=transaction_id)
            account = Account.objects.get(name=account_name)
            transaction.credit_account = account
            transaction.save()
            # Redirect to the same page after updating
            return redirect(request.META.get('HTTP_REFERER'))
        except (BankTransaction.DoesNotExist, Account.DoesNotExist) as e:
            # Handle the error accordingly
            print(f'Error updating transaction: {e}')
            # Redirect back with an error message or render a specific error template
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('transaction_list')  # Default redirect if not POST request


def get_all_accounting_transactions(request):
    try:
        transactions = AccountingTransaction.objects.all().order_by('-date')
        paginator = Paginator(transactions, 20)  # Show 10 transactions per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        account_names = Account.objects.values_list('name', flat=True)

        context = {
            "account_names": account_names,
            "transactions": transactions,
            "page_obj": page_obj,
        }

        return render(request, "transactions/accounts.html", context)
    except ValueError as e:
        return HttpResponse(f"ValueError: {e}")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")

class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

class AccountTransactionsView(View):
    def get(self, request, *args, **kwargs):
        custom_start_date = request.GET.get('start_date')
        custom_end_date = request.GET.get('end_date')
        period_offset = int(request.GET.get('period_offset', 0))

        if custom_start_date and custom_end_date:
            try:
                start_date = datetime.strptime(custom_start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(custom_end_date, '%Y-%m-%d').date()
                is_custom_range = True
            except ValueError:
                return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")
        else:
            end_date = timezone.now().date() - timedelta(days=28 * period_offset)
            start_date = end_date - timedelta(days=27)
            is_custom_range = False

        transaction_query = AccountingTransaction.objects.all().order_by('-debit_entry__date')
        if start_date and end_date:
            transaction_query = transaction_query.filter(debit_entry__date__gte=start_date, debit_entry__date__lte=end_date)

        paginator = Paginator(transaction_query, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        account_names = Account.objects.values_list('name', flat=True)

        context = {
            "account_names": account_names,
            "page_obj": page_obj,
            "start_date": start_date,
            "end_date": end_date,
            "is_custom_range": is_custom_range,
            "period_offset": period_offset,
            "prev_period": period_offset + 1,
            "next_period": period_offset - 1 if period_offset > 0 else None,
        }

        return render(request, "transactions/accounts.html", context)

    def post(self, request, *args, **kwargs):
        account_name = request.POST.get('account_name')
        account = get_object_or_404(Account, name=account_name)

        custom_start_date = request.GET.get('start_date')
        custom_end_date = request.GET.get('end_date')
        period_offset = int(request.GET.get('period_offset', 0))

        if custom_start_date and custom_end_date:
            try:
                start_date = datetime.strptime(custom_start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(custom_end_date, '%Y-%m-%d').date()
                is_custom_range = True
            except ValueError:
                return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")
        else:
            end_date = timezone.now().date() - timedelta(days=28 * period_offset)
            start_date = end_date - timedelta(days=27)
            is_custom_range = False

        transaction_query = AccountingTransaction.objects.filter(
            Q(credit_entry__account=account) | Q(debit_entry__account=account)
        ).order_by('-debit_entry__date')

        if start_date and end_date:
            transaction_query = transaction_query.filter(debit_entry__date__gte=start_date, debit_entry__date__lte=end_date)

        paginator = Paginator(transaction_query, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        account_names = Account.objects.values_list('name', flat=True)

        context = {
            "account_name": account_name,
            "account_names": account_names,
            "page_obj": page_obj,
            "start_date": start_date,
            "end_date": end_date,
            "is_custom_range": is_custom_range,
            "period_offset": period_offset,
            "prev_period": period_offset + 1,
            "next_period": period_offset - 1 if period_offset > 0 else None,
        }

        return render(request, "transactions/accounts.html", context)


def get_income_statement(request):
    budget_categories = BudgetSuperCategory.objects.all()
    accounts = Account.objects.exclude(name="Cash at bank")

    # Get custom date range if provided
    custom_start_date = request.GET.get('start_date')
    custom_end_date = request.GET.get('end_date')

    # Get the period offset for 4-week periods
    period_offset = int(request.GET.get('period_offset', 0))

    total_revenue = Decimal('0.00')
    total_expenses = Decimal('0.00')

    # Determine which date range to use
    if custom_start_date and custom_end_date:
        start_date = datetime.strptime(custom_start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(custom_end_date, '%Y-%m-%d').date()
        is_custom_range = True
    else:
        # Calculate 4-week period
        end_date = timezone.now().date() - timedelta(days=28 * period_offset)
        start_date = end_date - timedelta(days=27)
        is_custom_range = False

    for account in accounts:
        balance_query = AccountingEntry.objects.filter(account=account)

        # Apply date filters if provided
        if start_date:
            balance_query = balance_query.filter(date__gte=start_date)
        if end_date:
            balance_query = balance_query.filter(date__lte=end_date)

        total_amount = balance_query.aggregate(Sum('amount'))['amount__sum'] or 0
        account.balance = total_amount
        account.save()

        if account.name not in ["Inheritance", "Nomi salary", "Gunee salary"]:
            total_expenses += total_amount
        else:
            total_revenue += total_amount

    net_income = total_revenue - total_expenses

    categorised_accounts = {
        category.name: Account.objects.filter(budget_category=category).exclude(name="Cash at bank")
        for category in budget_categories
    }

    context = {
        "categorised_accounts": categorised_accounts,
        "budget_categories": budget_categories,
        "total_revenue": format(total_revenue, '.2f'),
        "total_expenses": format(total_expenses, '.2f'),
        "net_income": format(net_income, '.2f'),
        "start_date": start_date,
        "end_date": end_date,
        "is_custom_range": is_custom_range,
        "period_offset": period_offset,
        "prev_period": period_offset + 1,
        "next_period": period_offset - 1 if period_offset > 0 else None,
    }
    return render(request, "transactions/income_statement.html", context)


def get_account_analysis(request):
    account_name = request.POST.get('account_name')
    account = get_object_or_404(Account, name=account_name)

    transaction_query = AccountingTransaction.objects.filter(
        Q(credit_entry__account=account) | Q(debit_entry__account=account)
    ).order_by('-debit_entry__date')

    periods = get_monthly_periods()
    period_balances = {}

    for period in periods:
        start_date = period[0]
        end_date = period[1]
        balance_query = transaction_query.filter(date__gte=start_date, date__lte=end_date)
        total_amount = balance_query.aggregate(Sum('amount'))['amount__sum'] or 0
        # Format the key as "Month Year"
        period_key = start_date.strftime("%B %Y")

        period_balances[period_key] = total_amount

    # Convert period_balances to JSON
    period_balances_json = json.dumps(period_balances, cls=DecimalEncoder)

    context = {
        "account_name": account_name,
        'period_balances_json': period_balances_json,
    }

    return render(request, "transactions/account_analysis.html", context)
