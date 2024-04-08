import json
import psycopg2
import psycopg2.extras
import csv
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def connect(credentials_file='/home/gunee/Projects/Gunee/homeBudget/conf/local/db_credentials.json'):
    # Load database credentials from the JSON file
    with open(credentials_file, 'r') as file:
        credentials = json.load(file)

    # Establish a database connection
    conn = psycopg2.connect(
        host=credentials['hostname'],
        user=credentials['username'],
        password=credentials['password'],
        dbname=credentials['database'],
        port=credentials['port_id']
    )

    return conn


def close(conn):
    if conn is not None:
        conn.close()


def fetch_data_from_db(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM transactions")
        rows = cur.fetchall()

    # Convert the fetched data to a pandas DataFrame
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])

    return df


def add_transaction_records(conn, file):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # Read data from CSV file
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            script = "INSERT INTO transactions (member_id, date, amount, description, bank_balance, credit_account, debit_account) VALUES (%s, %s, %s, %s, %s, %s, %s);"  # Adjust column names accordingly

            # Iterate through CSV rows and insert into the database
            for row in csv_reader:
                date_value = row[0]
                amount_value = float(row[1]) if row[1] else None
                description_value = row[2]
                balance_value = float(row[3]) if row[3] else None
                member_id = 1  # Replace with actual member ID
                cur.execute(script, (member_id, date_value, amount_value, description_value, balance_value, None, None))

        # Commit the changes to the database
        conn.commit()


def add_transaction_category(conn, file):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
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

        # Constructing the INSERT statement
        insert_statement = "INSERT INTO accounts (name, keywords) VALUES (%s, %s);"

        # Iterate through JSON data and insert into the database
        for name, keywords in d.items():
            cur.execute(insert_statement, (name, keywords))

        # Commit the changes to the database
        conn.commit()


def get_accounts_info(conn):
    with conn.cursor() as cur:
        select_script = "SELECT account_id, name, type, budget_amount FROM accounts"
        cur.execute(select_script)
        values = cur.fetchall()

    # Extract the values from the fetched data and convert them into a list of tuples
    accounts_info = [(value[0], value[1], value[2], value[3]) for value in values]

    return accounts_info


def get_account_names_and_keywords(conn):
    with conn.cursor() as cur:
        select_script = "SELECT name, keywords FROM accounts"
        cur.execute(select_script)
        rows = cur.fetchall()

        # Convert the fetched data to a dictionary
    return {row[0]: row[1] for row in rows}


def add_expected_values(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # Start date
        start_month = datetime(2021, 7, 1)
        # End date
        end_month = datetime.now()

        def months_between(start_date, end_date):
            delta_years = end_date.year - start_date.year
            delta_months = end_date.month - start_date.month
            total_months = delta_years * 12 + delta_months
            return total_months

        # Number of months to insert data for
        num_months = months_between(start_month, end_month)

        # Transaction types
        transaction_types = {'Total Income': 6000, 'Total Expense': 5000, 'Total Debt Repayments': 500,
                             'Total Savings': 500}

        for transaction_type, amount in transaction_types.items():
            print(transaction_type)
            prev_month = start_month

            for i in range(num_months):
                this_month = prev_month + relativedelta(months=1)
                cur.execute("INSERT INTO expectations (transaction_type, date, amount) VALUES (%s, %s, %s)",
                            (transaction_type, this_month, amount))
                prev_month = this_month

        # Commit the changes to the database
        conn.commit()


def get_expected_total_values_by_type(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM expectations")
        rows = cur.fetchall()

    # Convert the fetched data to a pandas DataFrame
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
    # Convert 'date_column' to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['transaction_type'] = df['transaction_type'].str.strip()
    df['expected_value'] = df['expected_value'].astype(float)

    return df