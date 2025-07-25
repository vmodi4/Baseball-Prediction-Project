import streamlit as st
import statsapi
import pandas as pd

df = pd.read_csv("new_2025_mlb_dataset.csv")

# Show the first 5 rows
st.write(df.head())
st.write(len(df))
