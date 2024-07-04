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

from transactions.models import Account, BankTransaction, AccountingEntry, AccountingTransaction, BudgetSuperCategory


def print_write(l: list, m: models.Model):
    print(*l, sep='\n')
    m.objects.bulk_create(l)


def add_accounts():
    d = {
        "Revenue": {
            "Nomi salary": ["Daily", "Edited"],
            "Gunee salary": ["NANJID", "TSELMEG"],
            "Inheritance": ["gegeen", "ULZIIBADRAKH", "Finmo", "ADIYA"],
        },
        "Work-related": {
            "Work Expenses": ["Microsoft", "GITHUB", "RAILWAY", "CHATGPT", "LinkedIn", "OPENAI"],
        },
        "Living Expenses": {
            "Groceries": ["WOOLWORTHS", "TILBA", "THIRSTY", "COLES", "COSTCO", "ALDI", "M&J", "WW", "BAKERY", "MART", "IGA", "SUPA", "SUPAEXPRESS"],
            "Eating out": ["OMI", "DOMINOS", "EATS", "MENULOG", "GRILLD", "BWS", "CAFE", "Menulog", "Coffee", "Hungry", "MCDONALDS", "SUSHI", "KFC", "PIZZA", "BURGER", "Gelato", "COFFEE", "DONUTS", "Sharetea"],
            "Rent": ["Rental", "Ray", "White", "EDGE", "RENT", "DEFT"],
            "Electricity & Gas": ["AGL", "REAMPED", "ORIGIN"],
            "Mobile & Internet": ["VODAFONE", "Vodafone"],
            "Home": ["BUNNINGS", "Big", "W", "IKEA", "eBay", "AMAZON", "COTTON", "KATHMANDU", "KMART", "MKTPLC", "OFFICEWORKS", "Uniqlo", "UNIQLO", "SEPHORA", "ANACONDA"],
        },
        "Transportation": {
            "Public Transport": ["TRANSPORTFORNSW", "TRANSPORT"],
            "Petrol": ["Petroleum", "Caltex", "7-ELEVEN", "AMPOL", "BP", "ELEVEN"],
            "Rego": ["RMS", "SERVICE", "ACCESS"],
            "Parking": ["WILSON", "PARKING", "WIlsonParkingBenjamin", "WilsonParkingANUCanber"],
            "Car Insurance": ["BUDGET"],
        },
        "Personal": {
            "Grooming": ["CHEMIST", "HAIR"],
            "Health": ["Sport", "EYE", "Chemist", "PHARMACY", "Medical", "Fit", "Leisure", "Tsz"],
            "Entertainment": ["DISNEY", "AMZNPRIMEAU", "Disney", "Kindle", "YOUTUBEPREMIUM"],
            "Vices": ["KARKI", "STEAMGAMES", "LIQUORLAND", "STEAM", "SMOKE"],
            "Leisure and Travel": ["TOURSIM", "Hotel", "Booking", "BlocHaus"],
            "Gifts": ["GIFT", "PRESENT", "Hartog", "RMWilliams", "Gift"],
        },
        "Insurance": {
            "Insurance": ["BUPA"],
        },
        "Financial Expenses": {
            "Credit Cards": ["Credit", "Card", "CBA", "CREDIT", "ZipPay", "StepPay", "ZipMoney", "ZipMny"],
        },
        "Other Expenses": {
            "Other": ["Fee"],
            "Misc": [],
        },
        "Not Categorized": {
            "Cash Transfer": ["ATM", "CASH"],
            "Investments": ["Etoro"],
            "Emergency Fund": ["NETBANK"],
            "Cash at bank": ["CASH"],
        }
    }

    accounts = []

    for budget_category, subcategories in d.items():
        # Create or get the BudgetSuperCategory
        budget_super_category, _ = BudgetSuperCategory.objects.get_or_create(name=budget_category)

        for name, keywords in subcategories.items():
            # Check if the account already exists
            existing_account = Account.objects.filter(name=name).first()
            if existing_account is None:
                # If the account does not exist, create it
                account = Account(
                    name=name,
                    type="default_type",
                    keywords=keywords,
                    balance=0,
                    budget_category=budget_super_category
                )
                account.save()
                accounts.append(account)
            else:
                # If the account exists, update its budget category
                existing_account.budget_category = budget_super_category
                existing_account.save()
                accounts.append(existing_account)
    return accounts


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
    stop_words.update(
        {'value', 'date', 'card', 'au', 'aus', 'xx5824', 'canberra', 'sydney', 'melbourne', 'xx1656', 'DICKSON',
         'BRUCE', 'Fyshwick', 'xx7543'})

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
