# get the date formatting funciton later 

import pandas as pd
import statsapi
import streamlit as st

# get win_pct

def get_win_pct(wins, losses):
    if wins + losses == 0:
        return 0.0
    else:
        return wins / (wins + losses)
    


#data = statsapi.standings_data(division="all", include_wildcard=True, season= "2025", standingsTypes= None, date= "06/05/2025")

def get_team_info(team_id, date):
    data = statsapi.standings_data(division="all", include_wildcard=True, season= "2025", standingsTypes= None, date= date)
    for division_id, division_data in data.items():
        for team in division_data['teams']:
            if team['team_id'] == team_id:
                wins =  team["w"]
                losses = team["l"] 
                win_pct = get_win_pct(wins, losses)
                
                return win_pct

def get_home_and_away(team_id, date):
    
                
    




data = statsapi.standings_data(division="all", include_wildcard=True, season= "2025", standingsTypes= None, date= "06/05/2025")
for division_id, division_data in data.items():
    for team in division_data['teams']:
        if team['team_id'] == 143:
            new_data = team["w"]

st.write(data)
st.write(get_team_info(117, "06/05/2025"))  # Example date, adjust as needed
#st.write(new_data)  


# this should be the phillies. 

    