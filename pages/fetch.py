import pandas as pd
import numpy as np
import statsapi
import streamlit as st
import requests
import csv

# Write a quick function to obtain OBP for the team
def get_team_batting_stats_date(team_id, end_date):
    response = requests.get(f"https://statsapi.mlb.com/api/v1/teams/{team_id}/stats?stats=byDateRange&group=hitting&startDate=2025-03-18&endDate={end_date}")
    if response.status_code == 200:
        data = response.json()
        obp = data['stats'][0]['splits'][0]['stat']['obp']
        home_runs = data['stats'][0]['splits'][0]['stat']['homeRuns']
        ops = data['stats'][0]['splits'][0]['stat']['ops']
        return obp, home_runs, ops
    else:
        st.write(f"Error: {response.status_code}")
        return None, None, None

st.write(get_team_batting_stats_date(117, "2025-06-05"))  # Example date, adjust as needed

def get_pitching_stats_date(team_id, end_date):
    response = requests.get(f"https://statsapi.mlb.com/api/v1/teams/{team_id}/stats?stats=byDateRange&group=pitching&startDate=2025-03-18&endDate={end_date}")
    if response.status_code == 200: 
        data = response.json()
        era = data['stats'][0]['splits'][0]['stat']['era']
        whip = data['stats'][0]['splits'][0]['stat']['whip']
        strikeouts = data['stats'][0]['splits'][0]['stat']['strikeOuts']
        return era, whip, strikeouts
    else:
        st.write(f"Error: {response.status_code}")
        return None, None, None

def get_win_pct(wins, losses):
    if wins + losses == 0:
        return 0.0
    else:
        return wins / (wins + losses)

def get_team_win_pct(team_id, date):
    data = statsapi.standings_data(division="all", include_wildcard=True, season="2025", standingsTypes=None, date=date)
    for division_id, division_data in data.items():
        for team in division_data['teams']:
            if team['team_id'] == team_id:
                wins = team["w"]
                losses = team["l"]
                return wins, losses
    return 0, 0  # Default if team is not found

def convert_date(date):
    parts = date.split("-")
    if len(parts) != 3:
        raise ValueError("Input must be in 'YYYY-MM-DD' format")
    year, month, day = parts
    return f"{month}/{day}/{year}"

def get_all_stats(team_id, date):
    obp, home_runs, ops = get_team_batting_stats_date(team_id, date)
    era, whip, strikeouts = get_pitching_stats_date(team_id, date)
    new_date = convert_date(date)
    wins, losses = get_team_win_pct(team_id, new_date)
    win_pct = get_win_pct(wins, losses)
    return {
        "win_pct": win_pct,
        "obp": obp,
        "home_runs": home_runs,
        "ops": ops,
        "era": era,
        "whip": whip,
        "strikeouts": strikeouts
    }
st.write(get_all_stats(117, "2025-06-05"))  # Example date, adjust as needed

def get_game_winner(away_score, home_score):
    if away_score > home_score:
        return 0
    else:
        return 1

def create_csv_data_set(output_file, start_date, end_date):
    new_start_date = convert_date(start_date)
    new_end_date = convert_date(end_date)
    games = statsapi.schedule(start_date=new_start_date, end_date=new_end_date)

    header = [
        'home_win_pct', 'home_obp', 'home_home_runs', 'home_ops', 'home_era', 'home_whip', 'home_strikeouts',
        'away_win_pct', 'away_obp', 'away_home_runs', 'away_ops', 'away_era', 'away_whip', 'away_strikeouts',
        'is_home', 'game_winner'
    ]

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        # Loop through games and get gamePk
        for game in games:
            away_team_id = game['away_id']
            home_team_id = game['home_id']
            away_score = game['away_score']
            home_score = game['home_score']
            date = game['game_date']
            game_winner_label = get_game_winner(away_score, home_score)
            home_stats = get_all_stats(home_team_id, date)
            away_stats = get_all_stats(away_team_id, date)

            home_values = [
                home_stats['win_pct'], home_stats['obp'], home_stats['home_runs'],
                home_stats['ops'], home_stats['era'], home_stats['whip'], home_stats['strikeouts']
            ]

            away_values = [
                away_stats['win_pct'], away_stats['obp'], away_stats['home_runs'],
                away_stats['ops'], away_stats['era'], away_stats['whip'], away_stats['strikeouts']
            ]

            is_home = 1  # Assuming this is the home team, adjust as needed
            row = home_values + away_values + [is_home, game_winner_label]
            writer.writerow(row)

# Create the dataset
#$create_csv_data_set("new_2025_mlb_dataset.csv", "2025-03-29", "2025-07-23")
# uncomment if you want to create a new dataset again. 

# Load the dataset and display it
#df = pd.read_csv("mlb_dataset_june.csv")


