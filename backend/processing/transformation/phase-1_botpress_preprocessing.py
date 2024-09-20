import pandas as pd
import os
from typing import List, Dict

def load_chess_data() -> pd.DataFrame:
    csv_path = os.path.join('data', 'processed', 'chess_games_simple.csv')
    return pd.read_csv(csv_path)

def player_filter(df: pd.DataFrame, player: str) -> pd.DataFrame:
    return df[(df['white_player'] == player) | (df['black_player'] == player)]

def time_filter(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

def date_filter(df: pd.DataFrame, specific_date: str) -> pd.DataFrame:
    return df[df['date'] == specific_date]

def game_mode_filter(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    # Assuming 'time_control' column exists and contains game mode information
    return df[df['time_control'].str.contains(mode, case=False)]

def opponent_filter(df: pd.DataFrame, player: str, opponent: str) -> pd.DataFrame:
    return df[((df['white_player'] == player) & (df['black_player'] == opponent)) |
              ((df['black_player'] == player) & (df['white_player'] == opponent))]

def color_filter(df: pd.DataFrame, player: str, color: str) -> pd.DataFrame:
    if color.lower() == 'white':
        return df[df['white_player'] == player]
    elif color.lower() == 'black':
        return df[df['black_player'] == player]
    else:
        raise ValueError("Color must be 'white' or 'black'")

def preprocess_data(filters: Dict[str, str]) -> pd.DataFrame:
    df = load_chess_data()
    
    if 'player' in filters:
        df = player_filter(df, filters['player'])
    
    if 'start_date' in filters and 'end_date' in filters:
        df = time_filter(df, filters['start_date'], filters['end_date'])
    
    if 'specific_date' in filters:
        df = date_filter(df, filters['specific_date'])
    
    if 'game_mode' in filters:
        df = game_mode_filter(df, filters['game_mode'])
    
    if 'opponent' in filters:
        df = opponent_filter(df, filters['player'], filters['opponent'])
    
    if 'color' in filters:
        df = color_filter(df, filters['player'], filters['color'])
    
    return df

def get_user_filters() -> Dict[str, str]:
    filters = {}
    filters['player'] = input("Enter the player name: ")
    filters['start_date'] = input("Enter the start date (YYYY-MM-DD): ")
    filters['end_date'] = input("Enter the end date (YYYY-MM-DD): ")
    filters['specific_date'] = input("Enter a specific date (YYYY-MM-DD) or press Enter to skip: ")
    filters['game_mode'] = input("Enter the game mode (Blitz, Rapid, Classical, Bullet) or press Enter to skip: ")
    filters['opponent'] = input("Enter the opponent name or press Enter to skip: ")
    filters['color'] = input("Enter the color (White or Black) or press Enter to skip: ")
    
    # Remove empty filters
    return {k: v for k, v in filters.items() if v}

def main():
    filters = get_user_filters()
    filtered_df = preprocess_data(filters)
    print(f"Filtered dataset shape: {filtered_df.shape}")
    print(filtered_df.head())
    
    # Save the filtered dataset for TAPAS to use
    output_path = os.path.join('backend', 'processing', 'storage', 'filtered_chess_games.csv')
    filtered_df.to_csv(output_path, index=False)
    print(f"Filtered dataset saved to: {output_path}")

if __name__ == "__main__":
    main()
