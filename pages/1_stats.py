import streamlit as st
import statsapi

st.write("dashboard")

games = statsapi.schedule(start_date='08/01/2024',end_date='07/04/2025',team=143,opponent=121)


for x in games: 
    st.write(x['summary'])

st.write(statsapi.get('teams'))
