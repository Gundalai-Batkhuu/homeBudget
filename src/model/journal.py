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

    def get_total_expense_for_current_month(self):
        """
        Get the total monetary amount of all expense transactions for the current month
        :return:
        """
        sum = 0
        for transaction in self.transactions:
            if transaction.get_date().month == datetime.now().month and transaction.get_date().year == datetime.now().year and transaction.get_transaction_type() == "Expense":
                sum += transaction.get_amount()
        return sum

    def get_latest_cash_at_bank_balance(self):
        """
        Get the latest cash at bank balance
        :return:
        """
        return self.get_transactions()[0].get_bank_balance()






