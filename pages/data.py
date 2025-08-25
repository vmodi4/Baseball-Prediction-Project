import statsapi
from datetime import datetime, timedelta

import streamlit as st
from pages.fetch import convert_date
import joblib
from pages.fetch import get_all_stats
import pandas as pd
import requests
from supabase_client import supabase

def get_team_logo(team_id):
    url_endpoint = f"https://www.mlbstatic.com/team-logos/team-cap-on-dark/{team_id}.svg"
    response = requests.get(url_endpoint)
    if response.status_code == 200:
        return url_endpoint
    else:
        return None

model = joblib.load('mlb_rf_model.pkl')
current_date = datetime.now().strftime("%Y-%m-%d")

def get_team_logo(team_id):
    url_endpoint = f"https://www.mlbstatic.com/team-logos/team-cap-on-dark/{team_id}.svg"
    response = requests.get(url_endpoint)
    if response.status_code == 200:
        return url_endpoint
    else:
        return None


st.header(f"MLB Game Predictions for {current_date}")



# Define the column order manually (excluding the target)
model_columns = [
    "home_win_pct", "home_obp", "home_home_runs", "home_ops", "home_era", "home_whip", "home_strikeouts",
    "away_win_pct", "away_obp", "away_home_runs", "away_ops", "away_era", "away_whip", "away_strikeouts",
    "is_home"
]






def onClick(home_team_id, away_team_id, date, away_name, home_name):
    st.write("Placeholder for the llm portion")
@st.cache_data
def get_game_winner(game_status, winning_team):
    if game_status == "Final":
        return winning_team
    else:
        return 
    

def get_prediction(home_team_id, away_team_id, date):
    home_stats = get_all_stats(home_team_id, date)
    away_stats = get_all_stats(away_team_id, date)
    user_input = {
        "home_win_pct": home_stats['win_pct'],
        "home_obp": home_stats['obp'],
        "home_home_runs": home_stats['home_runs'],
        "home_ops": home_stats['ops'],
        "home_era": home_stats['era'],
        "home_whip": home_stats['whip'],
        "home_strikeouts": home_stats['strikeouts'],
        "away_win_pct": away_stats['win_pct'],
        "away_obp": away_stats['obp'],
        "away_home_runs": away_stats['home_runs'],
        "away_ops": away_stats['ops'],
        "away_era": away_stats['era'],
        "away_whip": away_stats['whip'],
        "away_strikeouts": away_stats['strikeouts'],
        "is_home": 1
    }

    input_df = pd.DataFrame([user_input])[model_columns]

# Make prediction
    prediction_from_model = model.predict(input_df)[0]
    prediction = int(prediction_from_model)  # Ensure it's a Python int, not numpy.int64

    prob_from_model = model.predict_proba(input_df)[0]
    prob = prob_from_model.tolist()  # [0.32, 0.68]
    

    return prediction, prob


rows = [st.columns(3) for _ in range(6)] 
new_tiles = [col for row in rows for col in row]

def get_new_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return convert_date(current_date)

def get_prev_date():
    prev_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    return convert_date(prev_date) 


actual_date = get_prev_date()



new_games = statsapi.schedule(start_date= actual_date, end_date= actual_date)
num_of_games = len(new_games)
correct_predictions = 0; 



i = 0
finalized_games = 0




for i, game in enumerate(new_games):
    if i>= len(new_tiles):
        break
    away_team_id = game['away_id']
    home_team_id = game['home_id']
    away_team_score = game['away_score']
    home_team_score = game['home_score']
    away_name = game['away_name']
    home_name = game['home_name']
    date = game['game_date']
    game_status = game['status']
    away_logo = get_team_logo(away_team_id)
    home_logo = get_team_logo(home_team_id)
    if game_status == "Final":
        winning_team = game['winning_team']
        finalized_games+=1

    else:
        winning_team = "Game not finished yet"


    
    prediction, prob= get_prediction(home_team_id, away_team_id, date)

    



    new_record = {
        "date": date,
        'away_logo': away_logo,
        'home_logo': home_logo,
        "away_name": away_name,
        "home_name": home_name,
        "prediction" : prediction,
        "prob": prob, 
        "away_team_score": away_team_score,
        "home_team_score": home_team_score,


    }

    existing = supabase.from_("records").select("*").eq("date", date).eq("away_name", away_name).eq("home_name", home_name).execute()

    
    
    if not existing.data:
          record = supabase.from_("records").insert(new_record).execute()

    


    


    #store predicted winner in a variable

    predicted_game_winner = home_name if prediction == 1 else away_name


    if(winning_team == predicted_game_winner):
        correct_predictions += 1
    else:
        correct_predictions += 0

    # now put all of these variables in a post request to the database



    
    
     
    

    


    data = {
    "date": date,
    "num_of_games": num_of_games,
    "correct_predictions": correct_predictions,
    "finalized_games": finalized_games,
  }
    
if finalized_games == num_of_games:
    response = supabase.from_("cumulative").insert(data).execute()






def display_prediction_summary():
    st.subheader("Prediction Summary for Day")
    st.write(f"Number of games for the day: {num_of_games}")
    st.write(f"Correct Predictions: {correct_predictions}")
    if(finalized_games == 0):
        st.write("No games have finished yet")
    else:
        st.write(f"Prediction Accuracy: {correct_predictions / finalized_games * 100:.2f}%" + f"({correct_predictions}/{finalized_games})")
   
    # instead of number of games, I need number of games that have finalized. 

    # testing


st.write(display_prediction_summary())
           #figure out how to cache data, search for particular games based on team name: 
         
        