import unittest
from src.model.model import Model
from src.model.database import connect, close
import decimal
from datetime import datetime


class TestModel(unittest.TestCase):
    conn = connect()
    model = Model(conn)
    close(conn)

    def test_number_of_transactions(self):
        transactions = self.model.get_transactions()
        self.assertEqual(len(transactions), 2799)

    def test_total_expense_for_current_month(self):
        result = self.model.get_total_expense_for_current_month()
        self.assertEqual(float(result), 1827.59)

    def test_account_transaction_values_for_month(self):
        result = self.model.get_account_transaction_values_for_month("Groceries", 2, 2024)
        self.assertEqual(float(result), 761.81)

    def test_account_expense_proportions_for_current_month(self):
        month = datetime.now().month
        year = datetime.now().year
        result = self.model.get_account_transaction_proportions_for_month_by_type("Expense", month, year)
        self.assertEqual(result, {'Cash Transfer': 0.0,
                                  'Eating out': 0.0,
                                  'Electricity & Gas': 0.0,
                                  'Entertainment': 0.0,
                                  'Groceries': 1.1019977128349356,
                                  'Grooming': 0.0,
                                  'Health': 0.0,
                                  'Home': 0.0,
                                  'Insurance': 0.0,
                                  'Misc': 78.7616478531837,
                                  'Mobile & Internet': 0.0,
                                  'Other': 0.025169759081632093,
                                  'Parking': 0.0,
                                  'Petrol': 0.0,
                                  'Public Transport': 0.0,
                                  'Rego': 0.0,
                                  'Rent': 0.0,
                                  'Vices': 0.0})

    def test_total_income_for_the_month(self):
        self.assertEqual(float(self.model.get_total_amount_of_transactions_by_type_for_given_month("Income", 2, 2024)),
                         6000.0)
        self.assertEqual(float(self.model.get_total_amount_of_transactions_by_type_for_given_month("Income", 1, 2024)),
                         11105.92)
        self.assertEqual(float(self.model.get_total_amount_of_transactions_by_type_for_given_month("Income", 12, 2023)),
                         39516.11)
        self.assertEqual(float(self.model.get_total_amount_of_transactions_by_type_for_given_month("Income", 11, 2023)),
                         10532.32)

    def test_cash_at_bank_balance_for_month(self):
        self.assertEqual(float(self.model.get_cash_at_bank_balance_by_month(2, 2024)), 7.48)
        self.assertEqual(float(self.model.get_cash_at_bank_balance_by_month(1, 2024)), 324.83)
        self.assertEqual(float(self.model.get_cash_at_bank_balance_by_month(12, 2023)), 89.40)

    def test_account_transaction_proportions_for_month_by_type(self):
        result = self.model.get_account_transaction_proportions_for_month_by_type("Income", 3, 2024)
        self.assertEqual(result, {'Cash Transfer': 0.0,
                                  'Eating out': 0.0,
                                  'Electricity & Gas': 0.0,
                                  'Entertainment': 0.0,
                                  'Groceries': 1.1019977128349356,
                                  'Grooming': 0.0,
                                  'Health': 0.0,
                                  'Home': 0.0,
                                  'Insurance': 0.0,
                                  'Misc': 78.7616478531837,
                                  'Mobile & Internet': 0.0,
                                  'Other': 0.025169759081632093,
                                  'Parking': 0.0,
                                  'Petrol': 0.0,
                                  'Public Transport': 0.0,
                                  'Rego': 0.0,
                                  'Rent': 0.0,
                                  'Vices': 0.0})

    def test_account_total_transaction_values_for_month_by_type(self):
        result = self.model.get_sum_of_transactions_for_each_account_by_type_for_month(3, 2024)
        self.assertEqual({'Cash Transfer': 6000.0}, result)

    def test_get_sum_of_transactions_for_each_account_by_type_for_month(self):
        income_account_proportions = self.model.get_sum_of_transactions_for_each_account_by_type_for_month(3, 2024)
        print(income_account_proportions)
        import pandas as pd
        df = pd.DataFrame.from_dict(income_account_proportions, orient='index', columns=['Value'])
        # Reset index to make the 'Misc' column a regular column
        df.reset_index(inplace=True)
        df.columns = ['Account', 'Value']
        print(df)
        self.assertEqual({'Account': {0: 'Misc'}, 'Value': {0: 6000.0}}, df.to_dict())



if __name__ == '__main__':
    unittest.main()
