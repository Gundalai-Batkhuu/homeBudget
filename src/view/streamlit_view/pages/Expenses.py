import streamlit as st

from src.view.streamlit_view.streamlit_plots import plot_all_transactions_for_month_table, \
    plot_monthly_cash_outflow_treemap_chart

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
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        key='month',
        placeholder='Select a month',
    )
    year = st.selectbox('Select a year',
                        [2022, 2023, 2024],
                        key='year',
                        placeholder='Select a year'
                        )

st.header('Expenses')
expense_account_proportions = st.session_state.model.get_account_expense_proportions_for_month_by_type("Expense", st.session_state.month, st.session_state.year)
debt_account_proportions = st.session_state.model.get_account_expense_proportions_for_month_by_type("Liability", st.session_state.month, st.session_state.year)
plot_monthly_cash_outflow_treemap_chart({**expense_account_proportions, **debt_account_proportions})