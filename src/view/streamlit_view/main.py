import streamlit as st

from src.main.Model.Model import Model
from src.main.Model.Database import create_db_connection

conn = create_db_connection()

model = Model(conn)


current_bank_balance = model.get_current_bank_balance()

st.title('Bank balance')
st.write(current_bank_balance)

