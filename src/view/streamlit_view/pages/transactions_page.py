import pandas as pd
import streamlit as st
from src.model.model import Model
from src.model.database import connect, close
from src.view.streamlit_view.streamlit_plots import plot_monthly_cash_outflow_treemap_chart, plot_all_transactions_for_month_table, \
    plot_cash_flow_summary
from datetime import datetime

st.set_page_config(
    page_title="Personal Finance Dashboard",
    layout="wide",
    page_icon="💰"
)


with st.sidebar:
    st.title("Personal Finance Dashboard")
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


st.header('Transactions list')
plot_all_transactions_for_month_table(st.session_state.model.get_all_transactions_for_month(st.session_state.month, st.session_state.year))
