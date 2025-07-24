import pandas as pd; 
import numpy as np; 

import statsapi; 

import streamlit as st; 

import requests

# Your MLB Stats API version (usually "v1")
import requests

player_id = 677594
team_id = 117
base_url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/stats"

params = {
    "stats": "byDateRange",
    "group": "hitting",
    "startDate": "2024-06-07",
    "endDate": "2024-08-07"
}

response = requests.get(base_url, params=params)
st.write(response)

if response.status_code == 200:
    data = response.json()
    st.write(data)
else:
    st.write(f"Error: {response.status_code}")



# from this I can get obp, home runs, and any other numerical team stat. 

#write quick function to obtain obb for the team

def get_team_batting_stats_date(team_id, end_date):
    response = requests.get(f"https://statsapi.mlb.com/api/v1/teams/{team_id}/stats?stats=byDateRange&group=hitting&startDate=2024-03-20&endDate={end_date}")
    if response.status_code == 200:
        data = response.json()
        obp = data['stats'][0]['splits'][0]['stat']['obp']
        home_runs = data['stats'][0]['splits'][0]['stat']['homeRuns']
        ops = data['stats'][0]['splits'][0]['stat']['ops']
        return obp, home_runs, ops
    else:
        st.write(f"Error: {response.status_code}")
        return None


def get_pitching_stats_date(team_id, end_date):
    response = requests.get(f"https://statsapi.mlb.com/api/v1/teams/{team_id}/stats?stats=byDateRange&group=pitching&startDate=2024-03-20&endDate={end_date}")
    if response.status_code == 200: 
        data = response.json()
        era = data['stats'][0]['splits'][0]['stat']['era']
        whip = data['stats'][0]['splits'][0]['stat']['whip']
        strikeouts = data['stats'][0]['splits'][0]['stat']['strikeOuts']
        return era, whip, strikeouts
# this function gets the team_obp from the start of the season to the
td = 117
end_date = "2024-06-07"
st.write(get_pitching_stats_date(td, end_date))


st.write(get_team_batting_stats_date(team_id, "2024-06-07"))

team_id2 = 117

new_data = statsapi.get('team_stats', {
    
    'stats': 'season',
    'group': 'pitching',
    'teamId': team_id2,
    'season': '2024'
})

st.write(new_data)


response2 = requests.get(f"https://statsapi.mlb.com/api/v1/teams/117/stats?stats=homeAndAway&group=hitting&season=2024")
st.write(response2)
data = response.json()

# trying to get the homeAndAway parameter to work in order to get home/away splits

#st.write(data)


   