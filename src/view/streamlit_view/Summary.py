import pandas as pd
import streamlit as st
from src.model.model import Model
from src.model.database import connect, close
from streamlit_plots import plot_monthly_cash_outflow_treemap_chart, plot_all_transactions_for_month_table, \
    plot_cash_flow_summary
from datetime import datetime

st.session_state.update(st.session_state)

st.set_page_config(
    page_title="Personal Finance Dashboard",
    layout="wide",
    page_icon="💰"
)


@st.cache_resource
def get_model():
    conn = connect()
    model = Model(conn)
    close(conn)
    return model


if 'month' not in st.session_state:
    st.session_state.month = datetime.now().month

if 'year' not in st.session_state:
    st.session_state.year = datetime.now().year

if 'model' not in st.session_state:
    st.session_state.model = get_model()

with st.sidebar:
    st.write("Month:", str(st.session_state.month), "Year:", str(st.session_state.year))

    month_name = st.selectbox(
        'Select a month',
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        key='month',
        placeholder='Select a month',
    )
    year = st.selectbox('Select a year',
                        [2022, 2023, 2024],
                        key='year',
                        placeholder='Select a year'
                        )

col1, col2 = st.columns([0.5, 0.5])

total_expense = st.session_state.model.get_sum_of_account_total_transaction_values_for_month_by_type("Expense",
                                                                                                     st.session_state.month,
                                                                                                     st.session_state.year)
total_debt_repayments = st.session_state.model.get_sum_of_account_total_transaction_values_for_month_by_type(
    "Liability", st.session_state.month, st.session_state.year)
total_income = float(
    st.session_state.model.get_total_amount_of_transactions_by_type_for_given_month("Income", st.session_state.month,
                                                                                    st.session_state.year))
total_savings = total_income - total_expense - total_debt_repayments  # Wrong

actual_total_values = pd.DataFrame({
    'transaction_type': ['Total Income', 'Total Expense', 'Total Debt Repayments', 'Total Savings'],
    'actual_values': [total_income, total_expense, total_debt_repayments, total_savings]
})

expected_total_values = st.session_state.model.get_expected_total_values_increment_by_transaction_type_for_month(
    st.session_state.month, st.session_state.year)

df = pd.merge(expected_total_values, actual_total_values)[['transaction_type', 'expected_value', 'actual_values']]

with col1:
    st.header('Cash flow summary')
    st.write("End of month cash at bank: ",
             "$" + str(st.session_state.model.get_cash_at_bank_balance_by_month(st.session_state.month, st.session_state.year)))
    st.table(df)

with col2:
    plot_cash_flow_summary(df)
