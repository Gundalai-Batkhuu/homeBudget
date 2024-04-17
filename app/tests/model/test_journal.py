from .fixture import model, journal, month, year, cursor


def test_get_sum_of_transactions_by_type_for_given_month(journal, month, year, cursor):
    query = f"SELECT sum(amount) FROM transactions WHERE date >= '01/02/2024' and date < '01/03/2024' and type = 'Income'"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    sum_value = journal.get_sum_of_transactions_by_type_for_given_month('Income', month, year)
    assert result == sum_value


def test_get_all_transactions_for_month(journal, month, year, cursor):
    query = f"SELECT count(*) FROM transactions WHERE date >= '01/02/2024' and date < '01/03/2024'"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    transactions = journal.get_all_transactions_for_month(month, year)
    assert len(transactions) == result


def test_get_cash_at_bank_balance_by_month(journal, month, year, cursor):
    query = f"SELECT bank_balance FROM transactions WHERE date >= '01/02/2024' and date < '01/03/2024' ORDER BY date DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    balance = journal.get_cash_at_bank_balance_by_month(month, year)
    assert result == balance


def test_get_sum_of_transactions_for_each_account_by_type_for_month(journal, month, year, cursor):
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
        sum_value = line[0]
        expected_result[acc_name] = sum_value

    actual_result = journal.get_sum_of_transactions_for_each_account_by_type_for_month('Income', month, year)
    assert expected_result == actual_result


def test_get_all_transactions_by_type_for_month(journal, month, year, cursor):
    query = f"SELECT count(*) FROM transactions WHERE date >= '01/02/2024' and date < '01/03/2024' and type = 'Income'"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    transactions = journal.get_all_transactions_by_type_for_month('Income', month, year)
    assert result == len(transactions)
