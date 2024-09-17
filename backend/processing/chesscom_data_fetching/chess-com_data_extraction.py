#!/usr/bin/env python
# coding: utf-8

import os
import requests
import pandas as pd
from datetime import datetime
import time

def extract_result_from_pgn(pgn):
    """
    Extract the game result from a PGN string.

    Args:
        pgn (str): The PGN string of a chess game.

    Returns:
        str: The result of the game ("1-0", "0-1", "1/2-1/2", or "Unknown").
    """
    if pgn:
        if "1-0" in pgn:
            return "1-0"
        elif "0-1" in pgn:
            return "0-1"
        elif "1/2-1/2" in pgn:
            return "1/2-1/2"
    return "Unknown"

def fetch_chess_games(usernames, year):
    """
    Fetch chess games data for given usernames and year from chess.com API.

    Args:
        usernames (list): List of chess.com usernames to fetch data for.
        year (int): The year for which to fetch game data.

    Returns:
        pandas.DataFrame: A DataFrame containing the fetched chess games data.
    """
    base_url = f"https://api.chess.com/pub/player"
    headers = {
        "User-Agent": os.environ.get("CHESS_COM_USERNAME", "default_username")
    }
    
    games_data = []
    
    for user in usernames:
        for month in range(1, 13):
            month_str = f"{year}/{month:02d}"
            url = f"{base_url}/{user}/games/{month_str}"

            response = requests.get(url, headers=headers)
            if response.status_code == 403:
                print(f"Access forbidden for URL: {url}")
                continue
            elif response.status_code == 404:
                print(f"No data for URL: {url}")
                continue
            elif response.status_code != 200:
                print(f"Failed to fetch data for URL: {url} with status code {response.status_code}")
                continue

            games = response.json().get("games", [])

            for game in games:
                pgn = game.get("pgn")
                game_info = {
                    "url": game.get("url"),
                    "pgn": pgn,
                    "time_control": game.get("time_control"),
                    "end_time": datetime.fromtimestamp(game.get("end_time")).strftime("%Y-%m-%d %H:%M:%S") if game.get("end_time") else None,
                    "rated": game.get("rated"),
                    "time_class": game.get("time_class"),
                    "rules": game.get("rules"),
                    "white_username": game["white"].get("username"),
                    "white_rating": game["white"].get("rating"),
                    "black_username": game["black"].get("username"),
                    "black_rating": game["black"].get("rating"),
                    "result": extract_result_from_pgn(pgn)
                }
                games_data.append(game_info)

            # Adding a delay to respect rate limits
            time.sleep(1)
    
    return pd.DataFrame(games_data)

def main():
    usernames = ["hikaru", "magnuscarlsen", "lachesisQ", "chesswarrior7197", "gukeshdommaraju", "gmwso", "lovevae", "fabianocaruana"]
    year = 2024
    df = fetch_chess_games(usernames, year)

    # Save DataFrame as CSV in data/raw folder
    csv_file = "./data/raw/chess_games_raw.csv"
    df.to_csv(csv_file, index=True)
    print(f"Raw data saved to {csv_file}")

if __name__ == "__main__":
    main()