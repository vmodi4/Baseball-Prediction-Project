import streamlit as st
import statsapi 
import csv


games = statsapi.schedule(start_date="06/01/2025", end_date="06/02/2025")
st.write(games)








#st.write(game_pk['away_name'])
#cards vs rockies