import streamlit as st
from src.model.model import Model
from src.model.database import create_db_connection, close_db_connection
from streamlit_plots import plot_monthly_cash_outflow_treemap_chart, plot_all_transactions_for_month_table, \
    plot_cash_flow_summary
from datetime import datetime

st.set_page_config(
    page_title="Personal Finance Dashboard",
    layout="wide",
    page_icon="💰"
)


@st.cache_resource
def get_model():
    conn = create_db_connection()
    model = Model(conn)
    close_db_connection(conn)
    return model


if 'month' not in st.session_state:
    st.session_state.month = datetime.now().month

if 'year' not in st.session_state:
    st.session_state.year = datetime.now().year

st.write("Month:", st.session_state.month, "Year:", st.session_state.year)

model = get_model()
cash_at_bank_balance = model.get_cash_at_bank_balance_by_month(st.session_state.month, st.session_state.year)

col1, col2, col3 = st.columns([0.2, 0.4, 0.4])


def change_date():
    st.session_state.month = datetime.strptime(month_name, "%B").month
    st.session_state.year = year
    st.experimental_rerun()


with col1:
    st.header('Bank balance')
    st.write("End of month cash at bank: ", cash_at_bank_balance)
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



with col2:
    st.header('Cash flow summary')

    total_expense = model.get_sum_of_account_total_transaction_values_for_month_by_type("Expense", st.session_state.month, st.session_state.year)
    total_debt_repayments = model.get_sum_of_account_total_transaction_values_for_month_by_type("Liability", st.session_state.month,
                                                                                                st.session_state.year)
    total_income = float(model.get_total_amount_of_transactions_by_type_for_given_month("Income", st.session_state.month, st.session_state.year))
    total_savings = total_income - total_expense - total_debt_repayments # Wrong

    plot_cash_flow_summary({'Total Income': total_income,
                            'Total Expense': total_expense,
                            'Total Debt Repayments': total_debt_repayments,
                            'Total Savings': total_savings})
with col3:
    st.header('Expenses')
    expense_account_proportions = model.get_account_expense_proportions_for_month_by_type("Expense", st.session_state.month, st.session_state.year)
    debt_account_proportions = model.get_account_expense_proportions_for_month_by_type("Liability", st.session_state.month, st.session_state.year)
    plot_monthly_cash_outflow_treemap_chart({**expense_account_proportions, **debt_account_proportions})

st.header('Transactions list')
plot_all_transactions_for_month_table(model.get_all_transactions_for_month(st.session_state.month, st.session_state.year))
