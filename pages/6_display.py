import statsapi
from datetime import datetime
import streamlit as st
from pages.fetch import convert_date
import joblib
from pages.fetch import get_all_stats
import pandas as pd





model = joblib.load('mlb_rf_model.pkl')

# Define the column order manually (excluding the target)
model_columns = [
    "home_win_pct", "home_obp", "home_home_runs", "home_ops", "home_era", "home_whip", "home_strikeouts",
    "away_win_pct", "away_obp", "away_home_runs", "away_ops", "away_era", "away_whip", "away_strikeouts",
    "is_home"
]




# Example: Simulate your get_all_stats() returning a dictionary of input values
user_input = {
    "home_win_pct": 0.56,
    "home_obp": 0.321,
    "home_home_runs": 98,
    "home_ops": 0.780,
    "home_era": 3.90,
    "home_whip": 1.22,
    "home_strikeouts": 910,
    "away_win_pct": 0.51,
    "away_obp": 0.310,
    "away_home_runs": 110,
    "away_ops": 0.750,
    "away_era": 4.01,
    "away_whip": 1.30,
    "away_strikeouts": 875,
    "is_home": 1
}

def onClick(home_team_id, away_team_id, date, away_name, home_name):
    st.write("Placeholder for the llm portion")

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
    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0]

    return prediction, prob


rows = [st.columns(3) for _ in range(6)] 
new_tiles = [col for row in rows for col in row]


current_date = datetime.now().strftime("%Y-%m-%d")
new_date = convert_date(current_date)
new_games = statsapi.schedule(start_date=current_date, end_date=current_date)
i = 0
for i, game in enumerate(new_games):
    if i>= len(new_tiles):
        break
    away_team_id = game['away_id']
    home_team_id = game['home_id']
    away_name = game['away_name']
    home_name = game['home_name']
    date = game['game_date']

    prediction, prob= get_prediction(home_team_id, away_team_id, date)

    

    with new_tiles[i]:
        tile = new_tiles[i].container(height = 300)
        with tile:
           st.write(f"🏟️ {away_name} vs {home_name} on {date}")
           st.write("🏠 Predicted Winner:", home_name if prediction == 1 else away_name)
           st.write("📊 Probabilities:", {away_name: round(prob[0], 5), home_name: round(prob[1], 5)})
           #figure out how to cache data, search for particular games based on team name: 
         
        
        
        
  

        
    

    



    
    

    # feed in these as parameters
    #st.write(game['away_name'], "vs", game['home_name'], "on", game['game_date'])
    #st.button("Predict Winner", key = game['away_id'], on_click = onClick)

    
   


  
    

  

   
    









'''current_date = datetime.now().strftime("%Y-%m-%d")
new_date = convert_date(current_date)
st.write(new_date)
new_games = statsapi.schedule(start_date=current_date, end_date=current_date)
for game in new_games:

    away_team_id = game['away_id']
    home_team_id = game['home_id']
    away_score = game['away_score']
    home_score = game['home_score']
    date = game['game_date']
    game_winner_label = get_game_winner(away_score, home_score)
    home_stats = get_all_stats(home_team_id, date)
    away_stats = get_all_stats(away_team_id, date)
    
    # display some info
    # have a streamlit button(to click predict game)
    st.write(game)



# def button_click(input right parameters):
# return model info. '''