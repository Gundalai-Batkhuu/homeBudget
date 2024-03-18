import streamlit as st
from src.model.model import Model
from src.model.database import create_db_connection, close_db_connection
from streamlit_plots import plot_monthly_expense_treemap_chart, plot_all_transactions_for_month_table
from datetime import datetime

conn = create_db_connection()
model = Model(conn)
close_db_connection(conn)

latest_cash_at_bank_balance = model.get_latest_cash_at_bank_balance()
curr_month = datetime.now().month
curr_year = datetime.now().year

st.title('Bank balance')
st.write(latest_cash_at_bank_balance)

st.title('Expenses')
expense_account_proportions = model.get_account_expense_proportions_for_current_month()
plot_monthly_expense_treemap_chart(expense_account_proportions)

st.title('Transactions list')
plot_all_transactions_for_month_table(model.get_all_transactions_for_month(curr_month, curr_year))