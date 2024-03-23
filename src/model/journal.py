from datetime import datetime
import pandas as pd


class Journal:
    transactions = list()

    def __init__(self):
        pass

    def get_transactions(self):
        """
        Get all transactions in the journal
        :return: A list of all transactions in the journal
        """
        return self.transactions

    def add_transaction(self, transaction):
        """
        Add a transaction the journal
        :param transaction: An AccountingTransaction object
        """
        self.transactions.append(transaction)

    def get_total_amount_of_transactions_by_type_for_given_month(self, trans_type: str, month: datetime.month, year: datetime.year):
        """
        Get the total monetary amount of all expense transactions of a type for the month
        :return:
        """
        sum = 0
        for transaction in self.transactions:
            if transaction.get_date().month == month and transaction.get_date().year == year and transaction.get_transaction_type() == trans_type:
                sum += transaction.get_amount()
        return sum

    def get_latest_cash_at_bank_balance(self):
        """
        Get the latest cash at bank balance
        :return:
        """
        return self.get_transactions()[0].get_bank_balance()

    def get_all_transactions_for_month(self, month: datetime.month, year: datetime.year):
        """
        Get all transactions for a specific month
        :param month:
        :param year:
        :return: A list of all transactions for a specific month
        """
        transactions = []
        for transaction in self.transactions:
            if transaction.get_date().month == month and transaction.get_date().year == year:
                transactions.append(transaction)
        return transactions





