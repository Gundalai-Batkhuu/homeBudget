from datetime import datetime
from src.main.Model import Account, Money
import unittest
from src.main.Model.Journal import Journal


class TestAccounting(unittest.TestCase):
    def setUp(self):
        self.journal = Journal()
        self.revenue = Account(0, "Revenue")
        self.deferred = Account(1, "Deferred")
        self.receivables = Account(2, "Receivables")
        self.revenue.withdraw(Money(500), self.receivables, datetime(2020, 1, 1))
        self.revenue.withdraw(Money(200), self.deferred, datetime(2020, 1, 1))


    def test_receivables_balance(self):
        self.assertEqual(Money(500).amount, self.receivables.current_balance().amount)

    def test_deferred_balance(self):
        self.assertEqual(Money(200).amount, self.deferred.current_balance().amount)

    def test_revenue_withdrawals(self):
        self.assertEqual(Money(-700).amount, self.revenue.current_balance().amount)


if __name__ == '__main__':
    unittest.main()

