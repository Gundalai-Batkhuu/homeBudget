import pandas as pd
import streamlit as st

from app.src.model.database import connect, close
from app.src.model.model import Model
from app.src.view.streamlit_view.streamlit_plots import plot_cash_flow_summary_bar_chart, \
    plot_actual_cash_allocation_pie_chart, plot_income_proportions_pie_chart
from datetime import datetime

st.session_state.update(st.session_state)

st.set_page_config(
    page_title="Personal Finance Dashboard",
    layout="wide",
    page_icon="💰"
)


@st.cache_resource
def get_model(conn_type):
    if conn_type == "streamlit":
        conn = st.connection("postgresql", type="sql")
        model = Model(conn, conn_type)
    elif conn_type == "psycopg2":
        conn = connect("app/conf/local/db_credentials.json")
        model = Model(conn, conn_type)
        close(conn)
    else:
        return "Error: Invalid connection type."
    return model


if 'month_name' not in st.session_state:
    st.session_state.month_name = datetime.now().strftime('%B')

if 'month' not in st.session_state:
    st.session_state.month = datetime.now().month
else:
    st.session_state.month = datetime.strptime(st.session_state.month_name, '%B').month

if 'year' not in st.session_state:
    st.session_state.year = datetime.now().year

if 'model' not in st.session_state:
    st.session_state.model = get_model("streamlit")
    #st.session_state.model = get_model("psycopg2")

with st.sidebar:
    month_name = st.selectbox(
        'Select a month',
        ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
         'December'],
        key='month_name',
        placeholder='Select a month',
    )
    year = st.selectbox('Select a year',
                        [2022, 2023, 2024],
                        key='year',
                        placeholder='Select a year'
                        )

total_expense = float(st.session_state.model.get_sum_of_account_total_transaction_values_for_month_by_type("Expense",
                                                                                                           st.session_state.month,
                                                                                                           st.session_state.year))
total_debt_repayments = st.session_state.model.get_sum_of_account_total_transaction_values_for_month_by_type(
    "Liability", st.session_state.month, st.session_state.year)
total_income = float(
    st.session_state.model.get_total_amount_of_transactions_by_type_for_given_month("Income", st.session_state.month,
                                                                                    st.session_state.year))
total_savings = total_income + total_expense + total_debt_repayments  # Wrong

actual_total_values = pd.DataFrame({
    'transaction_type': ['Total Income', 'Total Expense', 'Total Debt Repayments', 'Total Savings'],
    'actual_values': [total_income, total_expense, total_debt_repayments, total_savings]
})

expected_total_values = st.session_state.model.get_expected_total_values_increment_by_transaction_type_for_month(
    st.session_state.month, st.session_state.year)

total_values_by_transaction_type = pd.merge(expected_total_values, actual_total_values)[
    ['transaction_type', 'expected_value', 'actual_values']]

st.metric("Cash at bank",
          "$" + "{:.2f}".format(st.session_state.model.get_cash_at_bank_balance_by_month(st.session_state.month,
                                                                                         st.session_state.year)),
          delta=None, delta_color="normal", help=None, label_visibility="visible")

st.write("")
st.write("")
st.write("")

col11, col12, col13, col14 = st.columns([0.25, 0.25, 0.25, 0.25])

with col11:
    st.metric("Total income", "$" + "{:.2f}".format(total_income),
              delta=None, delta_color="normal", help=None, label_visibility="visible")

with col12:
    st.metric("Total expense", "$" + "{:.2f}".format(total_expense),
              delta=None, delta_color="normal", help=None, label_visibility="visible")

with col13:
    st.metric("Total debt repayments", "$" + "{:.2f}".format(total_debt_repayments),
              delta=None, delta_color="normal", help=None, label_visibility="visible")

with col14:
    st.metric("Total savings", "$" + "{:.2f}".format(total_savings),
              delta=None, delta_color="normal", help=None, label_visibility="visible")

st.write("")
st.write("")
st.write("")

col21, col22 = st.columns([0.5, 0.5])

with col21:
    plot_cash_flow_summary_bar_chart(total_values_by_transaction_type)

with col22:
    plot_actual_cash_allocation_pie_chart(total_values_by_transaction_type[['transaction_type', 'actual_values']])
