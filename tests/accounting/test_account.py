from datetime import datetime
import unittest
from src.model.model import Model
from src.model.database import create_db_connection, close_db_connection
import decimal


class TestAccounting(unittest.TestCase):
    conn = create_db_connection()
    model = Model(conn)
    close_db_connection(conn)

    def test_account_entries_for_month(self):
        month = datetime.now().month
        year = datetime.now().year

        account = self.model.ledger.get_account("Credit Cards")
        result = account.get_account_entries_for_month(month, year)

        self.assertEqual(5, len(result))

    def test_entries_sum_for_current_month(self):
        result = self.model.get_account_entries_sum_for_current_month("Credit Cards")
        self.assertEqual(367.55, float(result))
