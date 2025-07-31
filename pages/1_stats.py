import streamlit as st
import statsapi
import pandas as pd

df = pd.read_csv("new_2025_mlb_dataset.csv")\

schedule = statsapi.schedule(start_date="06/04/2025", end_date="06/05/2025")

for game in schedule:
    st.write(game)
    game_status = game['status']
    if(game_status == "Final"):
        winning_team = game['winning_team']
    else:
        winning_team = "Game not finished yet"
 

    st.write(winning_team)

team_id = 117

https://www.mlbstatic.com/team-logos/team-cap-on-dark/{teamId}.svg

url_endpoint = 'https://www.mlbstatic.com/team-logos/team-cap-on-dark/{team_id}.svg'
st.write(url_endpoint)


    # let's use this file to store the previous predictions and the acutao wine

    # connect database to this project. 

    # outline- create a drop down for previous dates: 
    # that date will be stored in a variable and then use schedule api to call all the games: 
    # then loop through to get all the winning teams 
    # I need to figure out how to store the model's predictions for each day: 

    # away_name 



# Show the first 5 rows


