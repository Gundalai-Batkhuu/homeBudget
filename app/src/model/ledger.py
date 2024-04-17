from datetime import datetime
from .account import Account


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
            budget_amount = account_info[3]
            self.accounts[name] = Account(id, name, type, budget_amount)

    def get_account(self, account_name) -> Account:
        return self.accounts[account_name]

    def get_account_entries(self, account_name):
        return self.get_account(account_name).get_entries()

    def get_account_entries_sum_for_month(self, account_name: str, month: int, year: int):
        """
        Get the total monetary amount of all transactions for a specific month
        :param account_name:
        :param month:
        :param year:
        :return: Sum of all transactions for a specific month
        """
        return self.get_account(account_name).get_account_entries_sum_for_month(month, year)

    def get_account_total_transaction_values_for_month_by_type(self, acc_type: str, month: datetime.month, year: datetime.year) -> {}:
        """
        Get the total expense values of all accounts of an account type for the month
        """

        result = {}
        for name, account in self.accounts.items():
            if account.type == acc_type:
                result[name] = float(account.get_account_entries_sum_for_month(month, year))
        return result

    def get_sum_of_account_total_transaction_values_for_month_by_type(self, acc_type: str, month: datetime.month, year: datetime.year):
        """
        Get the sum of all accounts of an account type for the month
        """
        accounts = self.get_account_total_transaction_values_for_month_by_type(acc_type, month, year)
        amount_sum = 0

        for account_name, amount in accounts.items():
            amount_sum += amount
        return amount_sum

    def get_account_expense_proportions_for_month_by_type(self, acc_type: str, month: datetime.month, year: datetime.year):
        """
        Get the proportion of each account of an account type from the sum of all accounts of that type
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
        accounts = self.get_account_total_transaction_values_for_month_by_type(acc_type, month, year)
        amount_sum = 0
        result = {}

        for account_name, amount in accounts.items():
            amount_sum += amount
        for account_name, amount in accounts.items():
            if amount_sum != 0:
                result[account_name] = (amount, float((amount / amount_sum) * 100))
            else:
                result[account_name] = (amount, 0)
        return result



