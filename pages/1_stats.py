import streamlit as st
import statsapi
import pandas as pd

df = pd.read_csv("new_2025_mlb_dataset.csv")\

schedule = statsapi.schedule(start_date="06/04/2025", end_date="06/05/2025")

for game in schedule:
    st.write(game)

    # away_name 



# Show the first 5 rows


