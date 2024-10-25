#!/usr/bin/env python
# coding: utf-8

import os
import asyncio
import aiohttp
import pandas as pd
from datetime import datetime
import logging
from tqdm import tqdm
import time

# Set up logging for Google Cloud Functions
logging.basicConfig(level=logging.ERROR)

class RateLimiter:
    def __init__(self, calls_per_minute):
        self.calls_per_minute = calls_per_minute
        self.calls_made = 0
        self.start_time = time.time()

    async def wait(self):
        self.calls_made += 1
        if self.calls_made >= self.calls_per_minute:
            elapsed = time.time() - self.start_time
            if elapsed < 60:
                await asyncio.sleep(60 - elapsed)
            self.calls_made = 0
            self.start_time = time.time()

rate_limiter = RateLimiter(60)  # 60 calls per minute

async def fetch_month_data(session, url, headers):
    await rate_limiter.wait()
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            return None

async def fetch_user_data(username, year, start_month, end_month, headers):
    base_url = f"https://api.chess.com/pub/player/{username}/games"
    async with aiohttp.ClientSession() as session:
        tasks = []
        for month in range(start_month, end_month + 1):
            url = f"{base_url}/{year}/{month:02d}"
            tasks.append(fetch_month_data(session, url, headers))
        return await asyncio.gather(*tasks)

def process_user_data(username, year, start_month, end_month):
    headers = {
        "User-Agent": os.environ.get("CHESS_COM_USERNAME", "default_username")
    }
    
    async def run_async():
        return await fetch_user_data(username, year, start_month, end_month, headers)
    
    month_data = asyncio.run(run_async())
    
    games_data = []
    for month, data in enumerate(month_data, start=start_month):
        if data and 'games' in data:
            for game in data['games']:
                game_info = {
                    "url": game.get("url"),
                    "time_control": game.get("time_control"),
                    "end_time": datetime.fromtimestamp(game.get("end_time")).strftime("%Y-%m-%d %H:%M:%S") if game.get("end_time") else None,
                    "rated": game.get("rated"),
                    "time_class": game.get("time_class"),
                    "rules": game.get("rules"),
                    "white_username": game["white"].get("username"),
                    "white_rating": game["white"].get("rating"),
                    "white_result": game["white"].get("result"),
                    "black_username": game["black"].get("username"),
                    "black_rating": game["black"].get("rating"),
                    "black_result": game["black"].get("result"),
                    "eco": game.get("eco"),
                    "fen": game.get("fen"),
                    "white_accuracy": game.get("accuracies", {}).get("white"),
                    "black_accuracy": game.get("accuracies", {}).get("black"),
                }
                games_data.append(game_info)
        else:
            logging.error(f"Error fetching data for {username} in {year}/{month:02d}")
    
    return games_data

def fetch_chess_games(usernames, year, start_month=1, end_month=12):
    all_games_data = []
    
    for username in tqdm(usernames, desc="Fetching user data"):
        user_games_data = process_user_data(username, year, start_month, end_month)
        all_games_data.extend(user_games_data)
    
    return pd.DataFrame(all_games_data)

def main():
    usernames = ["hikaru", "magnuscarlsen", "lachesisQ", "chesswarrior7197", "gukeshdommaraju", "gmwso", "lovevae", "fabianocaruana"]
    year = 2024
    start_month = 1
    end_month = 12
    df = fetch_chess_games(usernames, year, start_month, end_month)

    # Save DataFrame as CSV in data/raw folder
    csv_file = "./data/raw/chess_games_raw.csv"
    df.to_csv(csv_file, index=False)
    print(f"Raw data saved to {csv_file}")

if __name__ == "__main__":
    main()
