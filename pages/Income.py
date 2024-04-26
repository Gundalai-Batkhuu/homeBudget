import streamlit as st

from app.src.view.streamlit_view.streamlit_plots import plot_transactions_table, \
    plot_monthly_cash_outflow_treemap_chart, plot_income_proportions_pie_chart

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

st.header('Income')

income_account_proportions = st.session_state.model.get_sum_of_transactions_for_each_account_by_type_for_month(
    st.session_state.month, st.session_state.year)


plot_income_proportions_pie_chart(income_account_proportions)