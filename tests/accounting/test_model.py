import unittest
from src.model.model import Model
from src.model.database import create_db_connection, close_db_connection
import decimal


class TestAccounting(unittest.TestCase):
    conn = create_db_connection()
    model = Model(conn)
    close_db_connection(conn)

    def test_number_of_transactions(self):
        transactions = self.model.get_transactions()
        self.assertEqual(len(transactions), 2708)

    def test_cash_balance(self):
        cash_at_bank_balance = self.model.get_latest_cash_at_bank_balance()
        self.assertEqual(float(cash_at_bank_balance), 4172.89)

    def test_total_expense_for_current_month(self):
        result = self.model.get_total_expense_for_current_month()
        self.assertEqual(float(result), 1827.59)

    def test_account_transaction_values_for_month(self):
        result = self.model.get_account_transaction_values_for_month("Groceries", 2, 2024)
        self.assertEqual(float(result), 761.81)

    def test_account_expense_proportions_for_current_month(self):
        result = self.model.get_account_expense_proportions_for_current_month()
        self.assertEqual(result, {'Cash Transfer': 0.0,
             'Credit Cards': 20.111184674899732,
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

if __name__ == '__main__':
    unittest.main()

