from src.model import database as db
from src.model.account import AccountingTransaction
from src.model.journal import Journal
from src.model.ledger import Ledger
from src.model.money import Money
from datetime import datetime


class Model:
    journal = Journal()
    accounts_info: list
    conn = None
    ledger = None
    expected_total_values_by_type = None

    def __init__(self, conn):
        self.conn = conn
        df = db.fetch_data_from_db(conn)
        self.get_accounts_info()
        self.ledger = Ledger(self.accounts_info)
        self.expected_total_values_by_type = db.get_expected_total_values_by_type(self.conn)

        for index, row in df.iterrows():
            transaction = AccountingTransaction(
                row["transaction_id"],
                Money(row["amount"]),
                self.ledger.get_account(row["credit_account"]),
                self.ledger.get_account(row["debit_account"]),
                row["date"],
                row["credit_account"],
                row["description"],
                row["member_id"],
                row["type"],
                row["bank_balance"]
            )
            self.journal.add_transaction(transaction)

    def get_journal(self):
        return self.journal

    def get_transactions(self):
        """
        Get all transactions in the journal
        :return: List of all transactions in the journal
        """
        return self.journal.get_transactions()

    def get_total_expense_for_current_month(self):
        """
        Get the total monetary amount of all transactions for the current month
        :return: The total monetary amount of all transactions for the current month
        """
        return self.journal.get_sum_of_transactions_by_type_for_given_month("Expense", datetime.now().month, datetime.now().year)

    def get_all_account_total_transaction_value_for_month_by_type(self, acc_type: str, month: datetime.month, year: datetime.year):
        """
        Get the total monetary amount of all transactions of a specific account type for the current month
        """
        return self.ledger.get_account_total_transaction_values_for_month_by_type(acc_type, month, year)

    def get_account_transaction_values(self, account_name: str):
        return self.ledger.get_account_entries(account_name)

    def get_account_balance(self, account_name: str):
        return self.ledger.get_account(account_name).current_balance()

    def get_account_transaction_values_for_month(self, account_name: str, month: int, year: int):
        """
        Get the total monetary amount of all transactions of an account for a specific month
        :param account_name: The name of the account
        :param month: The month
        :param year: The year
        :return: The total monetary amount of all transactions for a specific month
        """
        return self.ledger.get_account_entries_sum_for_month(account_name, month, year)

    def get_accounts_info(self):
        self.accounts_info = db.get_accounts_info(self.conn)

    def get_account_transaction_proportions_for_month_by_type(self, acc_type: str, month: datetime.month, year: datetime.year):
        """
        Get the proportions of balances of accounts of a specific account type for the month
        """
        return self.ledger.get_account_expense_proportions_for_month_by_type(acc_type, month, year)


    def get_all_transactions_for_month(self, month, year):
        """
        Get all transactions for a specific month
        :param month:
        :param year:
        :return: A list of all transactions for a specific month
        """
        return self.journal.get_all_transactions_for_month(month, year)

    def get_sum_of_account_total_transaction_values_for_month_by_type(self, acc_type: str, month: datetime.month, year: datetime.year):
        """
        Get the sum of all accounts of an account type for the month
        """
        return self.ledger.get_sum_of_account_total_transaction_values_for_month_by_type(acc_type, month, year)

    def get_total_amount_of_transactions_by_type_for_given_month(self, trans_type, month, year):
        """
        Get the total monetary amount of all transactions of a specific type for the month
        :param trans_type:
        :param month:
        :param year:
        :return:
        """
        return self.journal.get_sum_of_transactions_by_type_for_given_month(trans_type, month, year)

    def get_cash_at_bank_balance_by_month(self, month: datetime.month, year: datetime.year):
        """
        Get the cash at bank balance for a specific month
        :param month:
        :param year:
        :return:
        """
        return self.journal.get_cash_at_bank_balance_by_month(month, year)

    def get_expected_total_values_increment_by_transaction_type_for_month(self, month, year):
        """
        Get the expected total values for a specific month
        """
        date = datetime(year, month, 1)
        return self.expected_total_values_by_type[self.expected_total_values_by_type['date'] == date]

    def get_account_total_transaction_values_for_month_by_type(self, acc_type, month, year):
        """
        Get the total monetary amount of all transactions of an account type for a specific month
        """
        return self.ledger.get_account_total_transaction_values_for_month_by_type(acc_type, month, year)

    def get_sum_of_transactions_for_each_account_by_type_for_month(self, month, year):
        """
        Get the sum of all transactions of a specific type for the month for each account
        """
        return self.journal.get_sum_of_transactions_for_each_account_by_type_for_month('Income', month, year)



