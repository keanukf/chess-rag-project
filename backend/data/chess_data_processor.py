import pandas as pd
import os
from datetime import datetime
import logging
import sqlite3

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary to map usernames to real names
username_to_realname = {
    # Example entries
    "Hikaru": "Hikaru Nakamura",
    "MagnusCarlsen": "Magnus Carlsen",
    "Firouzja2003": "Alireza Firouzja",
    "NikoTheodorou": "Nikos Theodorou",
    "DenLaz": "Deniz Laz",
    "Baku_Boulevard": "Rauf Mamedov",
    "lachesisQ": "Ian Nepomniachtchi",
    "ChessWarrior7197": "Nodirbek Abdusattorov",
    "GMWSO": "Wesley So",
    "LOVEVAE": "Wei Yi",
    "FabianoCaruana": "Fabiano Caruana"
}

def format_date_time(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")
    except ValueError:
        return date_str, ""  # Return original date and empty time if parsing fails

def load_data(input_csv_path):
    """Load raw chess data from a CSV file."""
    logger.info(f"Loading data from {input_csv_path}")
    return pd.read_csv(input_csv_path)

def select_essential_columns(df):
    """Exclude non-essential columns from the DataFrame."""
    logger.info("Excluding non-essential columns")
    columns_to_exclude = [
        "url", "fen"  # Example columns to exclude
        # Add more columns to exclude as needed
    ]
    return df.drop(columns=columns_to_exclude, errors='ignore')

def clean_and_format_data(df):
    """Clean and format the chess data."""
    logger.info("Cleaning and formatting data")
    df["date"], df["time"] = zip(*df["end_time"].apply(format_date_time))
    
    result_mapping = {
        "win": "win", "checkmated": "loss", "resigned": "loss", "timeout": "loss",
        "draw": "draw", "repetition": "draw", "agreed": "draw", "timevsinsufficient": "draw",
        "insufficient": "draw", "stalemate": "draw", "50move": "draw",
        "bughousepartnerlose": "loss", "abandoned": "loss"
    }
    
    df["white_result"] = df["white_result"].map(result_mapping)
    df["black_result"] = df["white_result"].apply(
        lambda x: "win" if x == "loss" else ("loss" if x == "win" else "draw")
    )
    
    df["white_realName"] = df["white_username"].map(username_to_realname).fillna("Unknown")
    df["black_realName"] = df["black_username"].map(username_to_realname).fillna("Unknown")
    
    return df

def save_data(df, output_csv_path):
    """Save the processed DataFrame to a CSV file."""
    logger.info(f"Saving processed data to {output_csv_path}")
    df.to_csv(output_csv_path, index=False)

def save_to_sqlite(df, db_name="chess_rag.db", table_name="super_gm_games_2024"):
    """Save the DataFrame to a SQLite database."""
    logger.info(f"Saving processed data to SQLite database {db_name}, table {table_name}")
    conn = sqlite3.connect(db_name)
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    finally:
        conn.close()

def main():
    # Get the directory path of the current file
    current_dir = os.path.dirname(__file__)
    
    # Define the paths relative to the current file's directory
    input_csv_path = os.path.join(current_dir, "chess_games_raw.csv")
    output_csv_path = os.path.join(current_dir, "chess_games_simple.csv")
    output_sqlite_path = os.path.join(current_dir, "chess_rag.db")

    # Load, process, and save the data
    df = load_data(input_csv_path)
    df = select_essential_columns(df)
    df = clean_and_format_data(df)
    save_data(df, output_csv_path)
    save_to_sqlite(df, output_sqlite_path)  # Save to SQLite database

# This part will only run if the script is executed directly (not when imported as a module)
if __name__ == "__main__":
    main()
