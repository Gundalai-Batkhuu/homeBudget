from django.contrib import admin
from .models import AccountingEntry, Account, AccountingTransaction, BankTransaction

# Register your models here.
admin.site.register(AccountingEntry)
admin.site.register(Account)
admin.site.register(AccountingTransaction)
admin.site.register(BankTransaction)