from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_bank_transactions, name="bank_transactions"),
    path("misc-transactions/", views.get_misc_bank_transactions, name="misc_bank_transactions"),
    path('update-debit-account/', views.update_debit_account, name='update_debit_account'),
    path('update-credit-account/', views.update_debit_account, name='update_credit_account'),
    path('get-all-accounting-transactions/', views.get_all_accounting_transactions, name='get_all_accounting_transactions'),
    path('get-account-transactions/', views.get_account_transactions, name='get_account_transactions'),
    path('get-budget/', views.get_budget, name='get_budget'),
]
