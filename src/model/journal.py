from datetime import datetime
import pandas as pd


class Journal:

    def __init__(self):
        self.transactions = []

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

    def get_sum_of_transactions_by_type_for_given_month(self, trans_type: str, month: datetime.month,
                                                        year: datetime.year):
        """
        Get the total monetary amount of all transactions of a type for the month
        :return:
        """
        sum = 0
        for transaction in self.get_all_transactions_by_type_for_month(trans_type, month, year):
            sum += transaction.get_amount()
        return sum

    def get_all_transactions_for_month(self, month: datetime.month, year: datetime.year):
        """
        Get all transactions for a specific month
        :param month:
        :param year:
        :return: A list of all transactions for a specific month
        """
        result = []
        for transaction in self.transactions:
            if transaction.get_date().month == month and transaction.get_date().year == year:
                result.append(transaction)
        return result

    def get_cash_at_bank_balance_by_month(self, month, year):
        """
        Get the cash at bank balance for a specific month
        :param month:
        :param year:
        :return: The cash at bank balance for a specific month
        """
        transactions = self.get_all_transactions_for_month(month, year)
        if transactions is None or len(transactions) == 0:
            return 0
        else:
            return transactions[0].get_bank_balance()

    def get_sum_of_transactions_for_each_account_by_type_for_month(self, trans_type, month, year):
        """
        Get the sum of all of a specific type for the month for each account
        :
        """
        result = {}
        for transaction in self.get_all_transactions_by_type_for_month(trans_type, month, year):
            if transaction.get_to_account() in result:
                result[transaction.get_to_account()] += transaction.get_amount()
            else:
                result[transaction.get_to_account()] = transaction.get_amount()
        return result

    def get_all_transactions_by_type_for_month(self, trans_type: str, month: datetime.month, year: datetime.year):
        """
        Get all transactions of a specific type
        :param trans_type : The type of transaction to filter by
        :return: A list of transactions of a specific type
        """

        result = []
        transactions = self.get_all_transactions_for_month(month, year)
        for transaction in transactions:
            if transaction.get_type() == trans_type:
                result.append(transaction)
        return result
