import csv
from datetime import datetime
from django.utils import timezone
import os
import django
from django.db import models

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from transactions.models import Account, BankTransaction, AccountingEntry, AccountingTransaction


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


def add_bank_transaction_records():
    data_directory = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir, 'data', '01_raw', '01_bank_account'))
    print(data_directory)
    dirs = os.listdir(data_directory)

    for file in dirs:
        if file.endswith(".csv"):
            print(file)
            file = os.path.normpath(
                os.path.join(os.path.dirname(__file__), os.pardir, 'data', '01_raw', '01_bank_account', file))
            with open(file, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                bank_transactions = []
                for row in csv_reader:
                    date_value = datetime.strptime(row[0], "%d/%m/%Y")
                    amount_value = float(row[1])
                    description_value = row[2]
                    bank_balance_value = float(row[3])

                    bank_transaction = BankTransaction(
                        date=date_value,
                        amount=amount_value,
                        description=description_value,
                        bank_balance=bank_balance_value
                    )
                    bank_transactions.append(bank_transaction)

                BankTransaction.objects.bulk_create(bank_transactions, ignore_conflicts=True)



if __name__ == "__main__":
    #seed_accounts()
    add_bank_transaction_records()
    print("Data inserted successfully!")
