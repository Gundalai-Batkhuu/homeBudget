import os
import csv
import csv
from datetime import datetime
from django.utils import timezone
import os
import django
from django.db import models

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from transactions.models import Account, BankTransaction, AccountingEntry, AccountingTransaction


def print_write(l: list, m: models.Model):
    print(*l, sep='\n')
    m.objects.bulk_create(l)


def add_accounts():
    d = {"Work Expenses": ["Microsoft", "GITHUB"],
        "Cash Transfer": ["ATM", "CASH"],
         "Credit Cards": ["Credit", "Card", "CBA", "CREDIT", "ZipPay", "StepPay", "ZipMoney"],
         "Inheritance": ["gegeen", "ULZIIBADRAKH", "Finmo"],
         "Nomi salary": ["Daily", "Edited"],
         "Gunee salary": ["NANJID", "TSELMEG"],
         "Groceries": ["WOOLWORTHS", "COLES", "COSTCO", "ALDI", "M&J", "WW", "BAKERY", "MART", "IGA", "SUPA"],
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
         "Vices": ["KARKI", "STEAMGAMES"],
         "Health": ["Sport", "EYE", "Chemist", "PHARMACY", "Medical"],
         "Entertainment": ["DISNEY"],
         "Cash at bank": ["CASH"],
         "Misc": []}

    accounts = []

    for name, keywords in d.items():
        # Check if the account already exists
        existing_account = Account.objects.filter(name=name).first()
        if existing_account is None:
            # If the account does not exist, create it
            account = Account(
                name=name,
                type="default_type",
                keywords=keywords,
                balance=0
            )
            account.save()


def get_bank_transaction_records():
    data_directory = os.path.normpath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, 'data', '01_raw', '01_bank_account'))
    dirs = os.listdir(data_directory)
    bank_transactions = []

    for file in dirs:
        if file.endswith(".csv"):
            file = os.path.normpath(
                os.path.join(data_directory, file))
            with open(file, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    bank_transactions.append(row)

    return bank_transactions


def process_description(text):

    # Tokenizes the text
    tokens = RegexpTokenizer(r'\w+').tokenize(text)

    # Removes stopwords and numeric values from a list of tokens
    stop_words = set(stopwords.words('english'))
    stop_words.update({'value', 'date', 'card', 'au', 'aus', 'xx5824', 'canberra', 'sydney', 'melbourne'})

    filtered_sentence = []
    for w in tokens:
        if w.lower() not in stop_words and not w.isnumeric():
            filtered_sentence.append(w)
    return filtered_sentence


def assign_category(tokens, amount_value):
    """Assigns debit and credit accounts to the transactions based on the keywords in tokens and amount value."""
    credit_account = Account.objects.get(name='Cash at bank')
    debit_account = Account.objects.get(name='Misc')

    accounts = Account.objects.all()
    account_data = {account.name: account.keywords for account in accounts}

    matched_account_name = None
    for name, keywords in account_data.items():
        if any(token in keywords for token in tokens):
            matched_account_name = name
            break

    if matched_account_name:
        if amount_value < 0:
            debit_account = Account.objects.get(name=matched_account_name)
        else:
            credit_account = Account.objects.get(name=matched_account_name)

    return debit_account, credit_account



def add_bank_transaction_records(transactions):
    bank_transactions = []
    for row in transactions:
        date_value = datetime.strptime(row[0], "%d/%m/%Y")
        amount_value = float(row[1])
        description_value = row[2]
        bank_balance_value = float(row[3])
        tokens = process_description(description_value)
        debit_account, credit_account = assign_category(tokens, amount_value)

        bank_transaction = BankTransaction(
            date=date_value,
            amount=amount_value,
            description=description_value,
            bank_balance=bank_balance_value,
            tokens=tokens,
            debit_account=debit_account,
            credit_account=credit_account
        )
        bank_transactions.append(bank_transaction)

    BankTransaction.objects.bulk_create(bank_transactions, ignore_conflicts=True)


