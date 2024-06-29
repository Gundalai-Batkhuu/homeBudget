from django.utils import timezone
import os
import django
from django.db import models

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from transactions.models import Account, Transaction, AccountingEntry


def print_write(l: list, m: models.Model):
    print(*l, sep='\n')
    m.objects.bulk_create(l)


def seed_accounts():
    d = {"Cash Transfer": ["ATM", "CASH"],
         "Credit Cards": ["Credit", "Card", "CBA", "CREDIT", "ZipPay", "StepPay"],
         "Inheritance": ["gegeen", "ULZIIBADRAKH", "Finmo"],
         "Nomi salary": ["Daily", "Edited"],
         "Gunee salary": ["NANJID", "TSELMEG"],
         "Groceries": ["WOOLWORTHS", "COLES", "COSTCO", "ALDI", "M&J", "WW", "BAKERY", "MART", "IGA"],
         "Eating out": ["OMI", "DOMINOS", "EATS", "MENULOG", "GRILLD", "BWS", "CAFE", "Menulog", "Coffee"],
         "Public Transport": ["TRANSPORTFORNSW"],
         "Petrol": ["Petroleum", "Caltex", "7-ELEVEN", "AMPOL"],
         "Rego": ["RMS", "SERVICE"],
         "Parking": ["WILSON"],
         "Car Insurance": ["BUDGET"],
         "Rent": ["Rental", "Ray", "White", "EDGE"],
         "Home": ["BUNNINGS", "Big", "W", "IKEA", "eBay"],
         "Grooming": ["CHEMIST", "HAIR"],
         "Insurance": ["BUPA"],
         "Mobile & Internet": ["VODAFONE"],
         "Electricity & Gas": ["AGL"],
         "Other": ["Fee"],
         "Investments": ["Etoro"],
         "Emergency Fund": ["NETBANK"],
         "Vices": ["KARKI"],
         "Health": ["Sport", "EYE", "Chemist"],
         "Entertainment": ["DISNEY"],
         "Cash": ["CASH"],
         "Misc": []}

    accounts = []

    for name, keywords in d.items():
        accounts.append(Account(
            name=name,
            type="default_type",
            keywords=keywords,
            balance=0
        ))

    print_write(accounts, Account)


if __name__ == "__main__":
    seed_accounts()
    print("Data inserted successfully!")
