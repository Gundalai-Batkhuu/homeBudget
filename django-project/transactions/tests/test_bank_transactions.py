from django.test import TestCase
from data_seed import add_bank_transaction_records
from transactions.models import BankTransaction
from transactions.util.bank_transactions import get_bank_transaction_records, add_accounts


class BankTransactionTestCase(TestCase):
    def setUp(self):
        add_accounts()
        add_bank_transaction_records(get_bank_transaction_records())
        self.bank_transactions = BankTransaction.objects.all()
        self.bank_transaction_records = get_bank_transaction_records()
        self.len_bank_transactions = len(self.bank_transactions)
        self.len_bank_transaction_records = len(self.bank_transaction_records)
        print(self.len_bank_transaction_records)
        self.bank_transaction_records_set = set(tuple(record) for record in self.bank_transaction_records)
        self.len_bank_transaction_records_set = len(self.bank_transaction_records_set)

    def test_transaction_count(self):
        self.assertNotEquals(self.len_bank_transactions, self.len_bank_transaction_records)

    def test_transaction_count_no_duplicates(self):
        self.assertEquals(self.len_bank_transactions, self.len_bank_transaction_records_set)
