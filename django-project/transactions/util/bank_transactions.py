import os
import csv


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

