from datetime import datetime
from src.main.Model import Account, Money
import unittest
from src.main.Model.Journal import Journal


class TestAccounting(unittest.TestCase):
    def setUp(self):
        self.journal = Journal()
        self.revenue = Account(0, "Revenue", self.journal)
        self.deferred = Account(1, "Deferred", self.journal)
        self.receivables = Account(2, "Receivables", self.journal)
        self.revenue.withdraw(Money(500), self.receivables, datetime(2020, 1, 1))
        self.revenue.withdraw(Money(200), self.deferred, datetime(2020, 1, 1))

    def test_transaction_count(self):
        self.assertEqual(2, len(self.journal.get_transactions()))


if __name__ == '__main__':
    unittest.main()