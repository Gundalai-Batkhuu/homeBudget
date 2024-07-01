from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_bank_transactions, name="bank_transactions"),
    path('update-debit-account/', views.update_debit_account, name='update_debit_account'),
]
