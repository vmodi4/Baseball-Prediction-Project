import streamlit as st
import statsapi

st.write("Welcome to the Profile Page")
data = statsapi.meta("statTypes")
st.write(data)