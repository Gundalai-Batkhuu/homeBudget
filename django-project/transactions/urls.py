from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_bank_transactions, name="bank_transactions"),
]