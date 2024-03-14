import unittest
from src.model.model import Model
from src.model.database import create_db_connection, close_db_connection


class TestAccounting(unittest.TestCase):
    def setUp(self):
        conn = create_db_connection()
        self.model = Model(conn)
        self.journal = self.model.journal
        close_db_connection(conn)

    def test_cash_balance(self):
        cash_at_bank_balance = self.model.get_latest_cash_at_bank_balance()
        self.assertEqual(cash_at_bank_balance, 4172.89)


if __name__ == '__main__':
    unittest.main()
