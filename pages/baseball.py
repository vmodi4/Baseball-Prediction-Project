import streamlit as st
import statsapi 
import csv


games = statsapi.schedule(start_date="07/28/2025", end_date="07/29/2025")
st.write(games)



# get the winning team and make sure status is "Final"








#st.write(game_pk['away_name'])
#cards vs rockies