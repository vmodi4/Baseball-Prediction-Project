import streamlit as st


st.write("Welcome to the MLB Game Prediction App! This application leverages machine learning to predict the outcomes of Major League Baseball games based on team statistics. Whether you're a baseball enthusiast or just curious about how data can inform sports predictions, you're in the right place!")

st.page_link("pages/6_display.py", label="Go to Prediction Display Page")

# unfortunately, streamlit does not support processes that run in the background. 

