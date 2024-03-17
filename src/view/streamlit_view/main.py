import streamlit as st

from src.model.model import Model
from src.model.database import create_db_connection, close_db_connection

conn = create_db_connection()

model = Model(conn)


latest_cash_at_bank_balance = model.get_latest_cash_at_bank_balance()

st.title('Bank balance')
st.write(latest_cash_at_bank_balance)

def get_chart_30299095():
    import plotly.express as px
    fig = px.treemap(
        names = ["Eve","Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parents = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
    )
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)

get_chart_30299095()

close_db_connection(conn)