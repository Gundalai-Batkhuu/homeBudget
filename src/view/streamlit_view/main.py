import streamlit as st

from src.model.model import Model
from src.model.database import create_db_connection

conn = create_db_connection()

model = Model(conn)


latest_cash_at_bank_balance = model.get_latest_cash_at_bank_balance()

st.title('Bank balance')
st.write(latest_cash_at_bank_balance)

