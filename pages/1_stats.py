
import statsapi
import pandas as pd
import requests


import streamlit as st
import datetime
from supabase_client import supabase
from streamlit_echarts import st_echarts


st.title("View Predictions from previous dates")

# Default to today's date
date = st.date_input(
    "Select a date",
    datetime.date.today()
)


games = supabase.from_("cumulative").select("*").eq("date", date.strftime("%Y-%m-%d")).execute()
st.write(games)

num_of_games = games.data[0]['num_of_games']
correct_predictions = games.data[0]['correct_predictions']
finalized_games = games.data[0]['finalized_games']

pie_data = [
    {"value": correct_predictions, "name": "Correct Predictions"},
    {"value": finalized_games - correct_predictions, "name": "Incorrect Predictions"},
    {"value": num_of_games - finalized_games, "name": "Unfinished Games"},
]

option = {
    "title": {"text": "Prediction Summary", "left": "center"},
    "tooltip": {"trigger": "item"},
    "legend": {"orient": "vertical", "left": "left"},
    "series": [
        {
            "name": "Predictions",
            "type": "pie",
            "radius": ["50%", "70%"],  # donut chart
            "avoidLabelOverlap": False,
            "itemStyle": {"borderRadius": 10, "borderColor": "#fff", "borderWidth": 2},
            "label": {"show": False, "position": "center"},
            "emphasis": {"label": {"show": True, "fontSize": "18", "fontWeight": "bold"}},
            "labelLine": {"show": False},
            "data": pie_data,
        }
    ],
}

st_echarts(options=option, height="400px")








response = supabase.from_("records").select("*").eq("date", date.strftime("%Y-%m-%d")).execute()






# got it in a response now show the data: 

rows = [st.columns(3) for _ in range(6)] 
new_tiles = [col for row in rows for col in row]

if not response.data:
    st.title("No games found for this date.")
else:
   for i, record in enumerate(response.data):
      if i>= len(new_tiles):
        break
      
      with new_tiles[i]:
        away_name = response.data[i]['away_name']
        home_name = response.data[i]['home_name']
        away_logo = response.data[i]['away_logo']
        home_logo = response.data[i]['home_logo']
        prob = response.data[i]['prob']
        prediction = response.data[i]['prediction']
        away_team_score = response.data[i]['away_team_score']
        home_team_score = response.data[i]['home_team_score']
        

        tile = new_tiles[i].container(height = 300)
        with tile:
           #st.image(away_team_id, width = 100)
           #st.image(home_team_id, width = 100)

           with st.container():
               st.image(away_logo, width=25)
               st.write(away_name)
               st.image(home_logo, width=25)
               st.write(home_name)

           winner = home_name if prediction == 1 else away_name
           st.markdown(f"Predicted Winner: <span style='color:lightgreen;'>{winner}</span>", unsafe_allow_html=True)
           st.write("📊 Probabilities:", {away_name: round(prob[0], 5), home_name: round(prob[1], 5)})
           st.write(f"Final Score: {away_name} {away_team_score} - {home_name} {home_team_score}")  
           
      



# in this page

