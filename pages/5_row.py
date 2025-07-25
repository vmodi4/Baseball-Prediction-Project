import statsapi
import streamlit as st

def get_game_winner(gamePk):
    


s

def create_game_row(gamePk, get_all_stats_fn):
    game = statsapi.get("game", {"gamePk": gamePk})
    date = game["gameDate"][:10]  # Format: YYYY-MM-DD

    home_id = game["teams"]["home"]["team"]["id"]
    away_id = game["teams"]["away"]["team"]["id"]

    # Get stats
    home_stats = get_all_stats_fn(home_id, date)  # Should return list or dict of 7 features
    away_stats = get_all_stats_fn(away_id, date)

    # Get label
    label = get_game_winner(gamePk)

    # Combine into one row
    row = {}

    for key, value in zip(["obp", "ops", "home_runs", "era", "whip", "strikeouts", "runs"], home_stats):
        row[f"home_{key}"] = value

    for key, value in zip(["obp", "ops", "home_runs", "era", "whip", "strikeouts", "runs"], away_stats):
        row[f"away_{key}"] = value

    row["home"] = 1  # or use one-hot separately if needed
    row["label"] = label

    return row