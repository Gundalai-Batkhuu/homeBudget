from src.model import database as db
from src.model.account import AccountingTransaction
from src.model.journal import Journal
from src.model.ledger import Ledger
from src.model.money import Money


class Model:
    journal = Journal()
    accounts_info: list
    conn = None
    ledger = None

    def __init__(self, conn):
        self.conn = conn
        df = db.fetch_data_from_db(conn)

        self.get_accounts_info()

        self.ledger = Ledger(self.accounts_info)
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
        return self.journal.get_total_expense_for_current_month()

    def get_account_entries_sum_for_current_month(self, account_name: str):
        return self.ledger.get_account_entries_sum_for_current_month(account_name)

    def get_all_accounts_total_expense_for_current_month(self):
        return self.ledger.get_all_account_total_expense_for_current_month()

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

    def get_account_expense_proportions_for_current_month(self):
        """
        Get the proportions of the account balances for the current month
        """
        return self.ledger.get_account_expense_proportions_for_current_month()

    def get_latest_cash_at_bank_balance(self):
        return self.journal.get_latest_cash_at_bank_balance()

    def get_all_transactions_for_month(self, month, year):
        """
        Get all transactions for a specific month
        :param month:
        :param year:
        :return: A list of all transactions for a specific month
        """
        return self.journal.get_all_transactions_for_month(month, year)