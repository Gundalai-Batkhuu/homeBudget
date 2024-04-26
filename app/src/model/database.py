import json
import psycopg2
import psycopg2.extras
import csv
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import boto3
import psycopg2
from botocore.exceptions import ClientError


def connect(credentials_file):
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


def fetch_data_from_db(conn, conn_type):
    if conn_type == "psycopg2":
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM transactions")
            rows = cur.fetchall()

        # Convert the fetched data to a pandas DataFrame
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
    elif conn_type == "streamlit":
        df = conn.query("SELECT * FROM transactions")
    else:
        return "Error: Invalid connection type."
    return df

def add_transaction_records(conn, file):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # Read data from CSV file
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            script = "INSERT INTO transactions (member_id, date, amount, description, bank_balance, credit_account, debit_account) VALUES (%s, %s, %s, %s, %s, %s, %s);"  # Adjust column names accordingly

            # Iterate through CSV rows and insert into the database
            for row in csv_reader:
                date_value = row[4]
                amount_value = float(row[1]) if row[1] else None
                description_value = row[5]
                balance_value = float(row[8]) if row[8] else None
                member_id = 1  # Replace with actual member ID
                credit_account = row[3]
                debit_account = row[2]
                cur.execute(script, (member_id, date_value, amount_value, description_value, balance_value, credit_account, debit_account))

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


def get_accounts_info(conn, conn_type):
    if conn_type == "psycopg2":
        with conn.cursor() as cur:
            select_script = "SELECT account_id, name, type, budget_amount FROM accounts"
            cur.execute(select_script)
            values = cur.fetchall()

        # Extract the values from the fetched data and convert them into a list of tuples
        accounts_info = [(value[0], value[1], value[2], value[3]) for value in values]
    elif conn_type == "streamlit":
        df = conn.query("SELECT account_id, name, type, budget_amount FROM accounts")
        accounts_info = [tuple(x) for x in df.to_records(index=False)]

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
                cur.execute("INSERT INTO expectations (transaction_type, date, expected_value) VALUES (%s, %s, %s)",
                            (transaction_type, this_month, amount))
                prev_month = this_month

        # Commit the changes to the database
        conn.commit()


def get_expected_total_values_by_type(conn, conn_type):
    if conn_type == "psycopg2":
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM expectations")
            rows = cur.fetchall()

        # Convert the fetched data to a pandas DataFrame
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
    elif conn_type == "streamlit":
        df = conn.query("SELECT * FROM expectations")

    # Convert 'date_column' to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['transaction_type'] = df['transaction_type'].str.strip()
    df['expected_value'] = df['expected_value'].astype(float)
    
    return df


def get_secret(secret_name, region_name):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']

    return secret


if __name__ == "__main__":
    secret_name = "rds!db-719c2fd1-423b-4e63-b785-7b616f975982"
    region_name = "ap-southeast-2"
    secret = get_secret(secret_name, region_name)

    secret_dict = json.loads(secret)

    username = secret_dict['username']
    passw = secret_dict['password']
    print(username)
    print(passw)

    try:
        conn = psycopg2.connect(host="terraform-20240419111553068200000001.cdf47oegxmwl.ap-southeast-2.rds.amazonaws.com",
                                port='5432',
                                database="homeBudget",
                                user=username,
                                password=passw)
        print("Connected to database")
    except psycopg2.DatabaseError as e:
        print("Error connecting to database")
        print(e)

    add_transaction_records(conn, "/home/gunee/Projects/Gunee/homeBudget/data/03_primary/fake_transactions.csv")

    conn.close()
    print("Connection closed")
