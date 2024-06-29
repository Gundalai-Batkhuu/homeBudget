from django.contrib import admin
from .models import AccountingEntry, Account, Transaction

# Register your models here.
admin.site.register(AccountingEntry)
admin.site.register(Account)
admin.site.register(Transaction)