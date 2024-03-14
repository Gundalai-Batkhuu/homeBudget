from datetime import datetime
import pandas as pd


class Journal:
    transactions = set()

    def __init__(self):
        pass

    def get_transactions(self):
        return self.transactions

    def set_transactions(self, transactions):
        self.transactions = transactions

    def add_transaction(self, transaction):
        self.transactions.add(transaction)

    def remove_transaction(self, transaction):
        self.transactions.remove(transaction)

    def get_transactions_values(self) -> list:
        result = []
        for transaction in self.transactions:
            result.append(transaction.get_value())

        return self.sort_transaction_values_by_descending_date(result)

    def get_account_transaction_values(self, account_name: str) -> list:
        result = []
        for transaction in self.transactions:
            if transaction.get_from_account() == account_name or transaction.get_to_account() == account_name:
                result.append(transaction.get_value())
        return self.sort_transaction_values_by_descending_date(result)

    def get_account_transaction_values_for_month(self, account_name: str, month: str, year: str) -> list:
        result = []
        selected_year = int(year)

        if month.isnumeric():
            selected_month = datetime.strptime(month, "%m").month
        else:
            selected_month = datetime.strptime(month, "%B").month

        for transaction in self.transactions:
            if transaction.get_from_account() == account_name or transaction.get_to_account() == account_name:
                if transaction.get_date().month == selected_month and transaction.get_date().year == selected_year:
                    result.append(transaction.get_value())
        return self.sort_transaction_values_by_descending_date(result)

    def sort_transaction_values_by_descending_date(self, transactions: list):
        # Define a custom key function to extract the id from each transaction
        def get_id(transaction):
            return transaction[0]

        # Sort the list of transactions using the custom key function
        return sorted(transactions, key=get_id, reverse=False)

    def sort_transaction_values_by_ascending_date(self, transactions: list):
        # Define a custom key function to extract the date from each sublist and reverse the sorting order
        def get_date(sublist):
            return sublist[0]

        # Sort the list of lists using the custom key function
        return sorted(transactions, key=get_date)

    def calculate_expense_increment_values(self, transactions: []):
        df = pd.DataFrame(self.sort_transaction_values_by_ascending_date(transactions),
                          columns=['Id', 'Date', 'From Account', 'To Account', 'Amount', 'Description', 'Account Owner',
                                   'Type', 'Bank Balance'])
        df = df[df["Type"] == 'Expense']
        df['Expenses'] = df['Amount'].cumsum()
        return df[['Date', 'Expenses']]

    def get_all_transaction_values_increment_for_current_month(self):
        data = []
        for transaction in self.transactions:
            if transaction.get_date().month == datetime.now().month and transaction.get_date().year == datetime.now().year:
                data.append(transaction.get_value())

        return self.calculate_expense_increment_values(data)

    def get_account_transaction_values_increment_for_current_month(self, account_name: str):
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        return self.calculate_expense_increment_values(
            self.get_account_transaction_values_for_month(account_name, month=month, year=year))

    def get_account_total_expense_for_current_month(self, account_name: str) -> list:
        result = []
        expense_increments = self.get_account_transaction_values_increment_for_current_month(account_name)
        result.append(account_name)
        if len(expense_increments) == 0:
            result.append(None)
            result.append(None)
        else:
            result.append(str(round(expense_increments['Expenses'].iloc[-1], 2)))
            result.append(expense_increments['Date'].iloc[-1].strftime('%d %B'))
        return result

    def get_all_account_total_expense_for_current_month(self, account_names) -> list[list]:
        result = []
        for name in account_names:
            if name != "Cash":
                result.append(self.get_account_total_expense_for_current_month(name))
        return result

    def get_account_proportions_for_current_month(self, account_names):
        data = self.get_all_account_total_expense_for_current_month(account_names)
        total_expense = 0
        result = []

        for i in range(len(data)):
            if data[i][1] is not None:
                result.append([data[i][0], data[i][1]])
                total_expense += float(data[i][1])

        for i in range(len(result)):
            result[i][1] = float(result[i][1]) / total_expense
        return result

    def get_latest_cash_at_bank_balance(self):
        return float(self.get_transactions_values()[0][-1])






