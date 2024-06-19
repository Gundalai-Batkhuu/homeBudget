import streamlit as st

from app.src.view.streamlit_view.streamlit_plots import plot_transactions_table, plot_monthly_cash_outflow_treemap_chart

st.session_state.update(st.session_state)

st.set_page_config(
    page_title="Personal Finance Dashboard",
    layout="wide",
    page_icon="💰"
)

with st.sidebar:
    st.write("Month:", str(st.session_state.month), "Year:", str(st.session_state.year))

    month_name = st.selectbox(
        'Select a month',
        ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        key='month_name',
        placeholder='Select a month',
    )
    year = st.selectbox('Select a year',
                        [2022, 2023, 2024],
                        key='year',
                        placeholder='Select a year'
                        )

st.header('Expenses')
expense_account_proportions = st.session_state.model.get_account_transaction_proportions_for_month_by_type("Expense", st.session_state.month, st.session_state.year)
debt_account_proportions = st.session_state.model.get_account_transaction_proportions_for_month_by_type("Liability", st.session_state.month, st.session_state.year)
plot_monthly_cash_outflow_treemap_chart({**expense_account_proportions, **debt_account_proportions})
expense_accounts_total = st.session_state.model.get_each_account_total_transaction_value_for_month_by_type("Expense", st.session_state.month, st.session_state.year)

st.table(expense_accounts_total)


st.write('Expense transactions list')
plot_transactions_table(st.session_state.model.get_all_transactions_by_type_for_month("Expense", st.session_state.month, st.session_state.year))