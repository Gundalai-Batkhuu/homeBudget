import unittest
from src.model.model import Model
from src.model.database import connect, close


class TestLedger(unittest.TestCase):
    conn = connect()
    journal = Model(conn).get_journal()
    close(conn)
    month = 2
    year = 2024

    def test_get_sum_of_transactions_by_type_for_given_month(self):
        conn = connect()
        cursor = conn.cursor()
        query = f"SELECT sum(amount) FROM transactions WHERE date >= '01/02/2024' and date < '01/03/2024' and type = 'Income'"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        sum = self.journal.get_sum_of_transactions_by_type_for_given_month('Income', self.month, self.year)
        self.assertEqual(result, sum)
        close(conn)


if __name__ == '__main__':
    unittest.main()
