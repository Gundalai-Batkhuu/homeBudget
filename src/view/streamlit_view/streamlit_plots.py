import pandas as pd
import plotly.express as px
import streamlit as st

def plot_monthly_cash_outflow_treemap_chart(expense_account_proportions: dict):
    acc_names = list(expense_account_proportions.keys())
    expense_amounts = [values[0] for values in expense_account_proportions.values()]
    percentages = [values[1] for values in expense_account_proportions.values()]

    fig = px.treemap(
        names=acc_names,
        parents=[''] * len(acc_names),
        values=expense_amounts,
        title='Actual allocation summary',
        width=600,
        height=400
    )


    # Assign custom data to each trace
    fig.update_traces(customdata=list(zip(expense_amounts, percentages)))
    # Update hover template to include custom data
    fig.update_traces(hovertemplate='%{label}<br>Expense: $%{customdata[0]}<br>Percentage: %{customdata[1]:.2f}%')
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    st.plotly_chart(fig, theme="streamlit")


def plot_all_transactions_for_month_table(transactions: list):
    date = [transaction.date for transaction in transactions]
    description = [transaction.description for transaction in transactions]
    amount = [transaction.money.amount for transaction in transactions]
    account_name = [transaction.to_acc.name for transaction in transactions]

    df = pd.DataFrame(data=zip(date, account_name, amount, description),
                      columns=['Date', 'Category', 'Amount', 'Description'])
    st.dataframe(df,
                 hide_index=True, )


def plot_cash_flow_summary(df: pd.DataFrame):
    st.table(df)
    # Create a bar chart using Plotly
    fig = px.bar(df, y='transaction_type', x=['amount', 'actual_values'], barmode='group',
                 labels={'value': 'Values', 'transaction_type': 'Transaction Type'},
                 width=500,
                 height=400,
                 orientation='h')
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        legend_title=None,
    )
    st.plotly_chart(fig)

