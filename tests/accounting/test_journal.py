import unittest
from src.model.model import Model
from src.model.database import connect, close
import decimal
from datetime import datetime


class TestJournal(unittest.TestCase):
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

    def test_get_all_transactions_for_month(self):
        conn = connect()
        cursor = conn.cursor()
        query = f"SELECT count(*) FROM transactions WHERE date >= '01/02/2024' and date < '01/03/2024'"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        transactions = self.journal.get_all_transactions_for_month(self.month, self.year)
        self.assertEqual(len(transactions), result)
        close(conn)

    def test_get_cash_at_bank_balance_by_month(self):
        conn = connect()
        cursor = conn.cursor()
        query = f"SELECT bank_balance FROM transactions WHERE date >= '01/02/2024' and date < '01/03/2024' ORDER BY date DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        balance = self.journal.get_cash_at_bank_balance_by_month(self.month, self.year)
        self.assertEqual(result, balance)
        close(conn)

    def test_get_sum_of_transactions_for_each_account_by_type_for_month(self):
        conn = connect()
        cursor = conn.cursor()
        query = '''
        SELECT sum(amount), debit_account FROM transactions 
        WHERE date >= '01/02/2024' and date < '01/03/2024' and type = 'Income'
        group by debit_account
        '''
        cursor.execute(query)
        query_result = cursor.fetchall()
        expected_result = {}
        for line in query_result:
            acc_name = line[1]
            sum = line[0]
            expected_result[acc_name] = sum

        actual_result = self.journal.get_sum_of_transactions_for_each_account_by_type_for_month('Income', self.month, self.year)
        self.assertEqual(expected_result, actual_result)

    def test_get_all_transactions_by_type_for_month(self):
        conn = connect()
        cursor = conn.cursor()
        query = f"SELECT count(*) FROM transactions WHERE date >= '01/02/2024' and date < '01/03/2024' and type = 'Income'"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        transactions = self.journal.get_all_transactions_by_type_for_month('Income', self.month, self.year)
        self.assertEqual(result, len(transactions))
        close(conn)


if __name__ == '__main__':
    unittest.main()
