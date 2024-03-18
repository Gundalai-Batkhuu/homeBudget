from datetime import datetime
from src.model.account import Account


class Ledger:
    accounts = dict()
    accounts_info: list

    def __init__(self, accounts_info: list):
        self.accounts_info = accounts_info

        for account_info in self.accounts_info:
            # Form: ['ID', 'Name', 'Type']
            name = account_info[1]
            id = account_info[0]
            type = account_info[2]  # Type is either 'Asset', 'Liability', 'Equity', 'Income', or 'Expense'
            self.accounts[name] = Account(id, name, type)

    def get_account(self, account_name) -> Account:
        return self.accounts[account_name]

    def get_account_entries(self, account_name):
        return self.get_account(account_name).get_entries()

    def get_account_entries_sum_for_current_month(self, account_name):
        return self.get_account(account_name).get_entries_sum_for_current_month()

    def get_account_entries_sum_for_month(self, account_name: str, month: int, year: int):
        """
        Get the total monetary amount of all transactions for a specific month
        :param account_name:
        :param month:
        :param year:
        :return: Sum of all transactions for a specific month
        """
        return self.get_account(account_name).get_account_entries_sum_for_month( month, year)

    def get_all_account_total_expense_for_current_month(self) -> {}:
        """
        Get the total expense values of all expense accounts for the current month
        :return: Dictionary with account name as key and total expense as value
        """
        result = {}
        for name, account in self.accounts.items():
            if account.type == "Expense":
                result[name] = float(account.get_entries_sum_for_current_month())
        return result

    def get_account_expense_proportions_for_current_month(self):
        """
        Get the proportion of each expense account from the total expense
        for the current month
        :return:
        select
        debit_account,
        sum(amount) as acc_sum,
        sum(amount) * 100 /
        (select sum(amount)
        from transactions
        where date >= '2024-03-01' and debit_account != 'Cash')
        as proportion
        from transactions
        where date >= '2024-03-01' and debit_account != 'Cash'
        group by debit_account
        """
        expense_accounts = self.get_all_account_total_expense_for_current_month()
        total_expense = 0
        result = {}

        for account_name, expense in expense_accounts.items():
            total_expense += expense
        for account_name, expense in expense_accounts.items():
            result[account_name] = (expense, float((expense / total_expense) * 100))
        return result
