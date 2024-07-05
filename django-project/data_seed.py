from transactions.util.bank_transactions import add_bank_transaction_records, add_accounts, \
    get_bank_transaction_records, add_accounting_transactions

add_accounts()
add_bank_transaction_records(get_bank_transaction_records())
add_accounting_transactions()
print("Data inserted successfully!")
