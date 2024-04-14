from datetime import datetime
import unittest
from src.model.model import Model
from src.model.database import connect, close
import decimal


class TestAccounting(unittest.TestCase):
    conn = connect()
    model = Model(conn)
    close(conn)

    def test_account_entries_for_month(self):
        month = datetime.now().month
        year = datetime.now().year

        account = self.model.ledger.get_account("Credit Cards")
        result = account.get_account_entries_for_month(month, year)

        self.assertEqual(5, len(result))


